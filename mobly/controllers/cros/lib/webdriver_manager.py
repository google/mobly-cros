# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A manager for webdriver related operations on a ChromeOS device.

Reference:
https://chromium.googlesource.com/chromiumos/third_party/autotest/+/refs/heads/main/client/common_lib/cros/chromedriver.py
"""

import http
import logging
import re
from typing import Optional
import urllib.error
import urllib.request

from selenium import webdriver as selenium_webdriver
from selenium.common import exceptions as selenium_exceptions

import retry
import functools

from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import ssh as ssh_lib
from mobly.controllers.cros.lib import unix_utils


# Per (internal), after the webdriver is set up, the URL below indicates that
# the webdriver is broken and many functionalities won't work.
_WEBDRIVER_SETUP_FAIL_URL = (
    'chrome-extension://lmjegmlicamnimmfhcmpkclmigmmcbeh/offscreen.html'
)


class Error(Exception):
  """Raised for errors related to the webdriver manager module."""


class WebDriverSetupError(Exception):
  """Raised for errors if failed to setup webdriver."""

class NotExpectedValueError(Exception):
  """Raise for errors if function called and get unexpected return."""


def verify_result(expected_result):
  """A decorator that verifies the result of a function against an expected result.

  Args:
      expected_result: The expected result to compare against.
  Excepts:
      NotExpectedValueError: If the result of the function does not match the
      expected result.
  Returns:
      A decorator that wraps the function.
  """

  def decorator(func):
    @functools.wraps(func)  # Preserves original function's metadata
    def wrapper(*args, **kwargs):
      actual_result = func(*args, **kwargs)

      if actual_result != expected_result:
        error_message = (
            f"Function '{func.__name__}' returned unexpected result: "
            f'Expected: {expected_result}, Actual: {actual_result}'
        )

        raise NotExpectedValueError(error_message)
      return actual_result

    return wrapper  # Return the wrapped function
  return decorator  # Return the decorator itself


# TODO: Remove this class after we solved the flakiness issue.
class _WebDrvierRemote(selenium_webdriver.Remote):
  """Override the super class to print more logs for debugging."""

  def execute(self, driver_command, params=None):
    """See docstring in super class."""
    if self.session_id is not None:
      if not params:
        params = {'sessionId': self.session_id}
      elif 'sessionId' not in params:
        params['sessionId'] = self.session_id

    params = self._wrap_value(params)
    response = self.command_executor.execute(driver_command, params)

    # Modification begin.
    # Compared with the impl of super class, we add this log message.
    logging.debug(
        'Webdriver client executed command with response: %s', response
    )
    # modification end.

    if response:
      self.error_handler.check_response(response)
      response['value'] = self._unwrap_value(response.get('value', None))
      return response
    # If the server doesn't send a response, assume the command was
    # a success
    return {'success': 0, 'value': None, 'sessionId': self.session_id}


class WebDriverManager:
  """A manager manages the lifecycle of the webdriver for a CrOS device.

  The setup steps for running remote webdriver:
  1. Forwards the local port to the remote chromedriver server port.
  2. Starts the chromedriver server on the CrOS device. (executor)
  3. Queries the debugging port of the Chrome on the CrOS device. (debugger)
  4. Builds the remote webdriver instance with the debugger/executor address

  The teardown steps for ending remote webdriver:
  1. Closes/Quits the remote webdriver
  2. Stops the chromedriver server on the CrOS device.
  3. Ends the test will stop the daemon thread for port forwarding.

  Attributes:
    webdriver: the underlying remote webdriver object.
  """

  _local_forwarded_chromedriver_port: int | None = None
  _remote_chrome_debugging_port: int | None = None

  def __init__(
      self,
      ssh: ssh_lib.SSHProxy,
      logger: logging.LoggerAdapter,
      ssh_forward_local_port: int = 0,
      chromedriver_server_port: int = 4444,
  ) -> None:
    """Initializes the WebDriverManager instance.

    Args:
      ssh: The ssh connection to the ChromeOS device.
      logger: The logger adapter for the ChromeOS device.
      ssh_forward_local_port: The port on the local machine for ssh port
        forwarding.
      chromedriver_server_port: The port number for the chromedriver server on
        the CrOS device.
    """
    self._chromedriver_server_port = chromedriver_server_port
    self._log = logger
    self._remote_chromedriver_server_process = None
    self._ssh = ssh
    self._ssh_forward_local_port = ssh_forward_local_port
    self._webdriver = None
    self._need_teardown = False

  @property
  def webdriver(self) -> Optional[selenium_webdriver.Remote]:
    """The remote webdriver object for the CrOS device."""
    return self._webdriver

  @retry.retry(exceptions=WebDriverSetupError, tries=3, delay=5)
  def setup(self) -> selenium_webdriver.Remote:
    """The entry point for setting up the remote webdriver.

    Returns:
      The remote webdriver instance.

    Raises:
      Error: if fail to find or parse the command of the chrome process.
    """
    self._log.debug('Starting setup the webdriver.')
    self._need_teardown = True
    self._forward_chromedriver_server_port()
    self._start_remote_chromedriver_server()
    self._get_remote_chrome_debugging_port()
    self._webdriver = self._build_webdriver()

    try:
      self._validate_webdriver_setup()
    except WebDriverSetupError:
      self._log.debug(
          'Error occurred when trying to setup webdriver, stopping it.'
      )
      self.teardown()
      raise

    # switch to the latest created tab.
    self._webdriver.switch_to.window(self._webdriver.window_handles[-1])
    self._log.debug('Successfully setup the webdriver.')
    return self._webdriver

  def __del__(self):
    self.teardown()

  def teardown(self) -> None:
    """Tears the remote webdriver object down."""
    if not self._need_teardown:
      return

    self._log.debug('Starting teardown the webdriver.')
    self._stop_webdriver()
    self._clear_remote_chrome_debugging_port()
    self._stop_remote_chromedriver_server()
    self._stop_port_forwarding()
    self._need_teardown = False
    self._log.debug('Successfully teardown the webdriver.')

  def _forward_chromedriver_server_port(self) -> None:
    """Forwards the local port to the remote chromedriver server port."""
    self._local_forwarded_chromedriver_port = self._ssh.forward_port(
        self._chromedriver_server_port, local_port=self._ssh_forward_local_port
    )
    self._log.debug(
        'Forward local port %d to remote chromedriver server port %d.',
        self._local_forwarded_chromedriver_port,
        self._chromedriver_server_port,
    )

  def _stop_port_forwarding(self) -> None:
    if self._local_forwarded_chromedriver_port:
      self._ssh.stop_port_forwarding(self._local_forwarded_chromedriver_port)
      self._local_forwarded_chromedriver_port = None

  def _start_remote_chromedriver_server(self) -> None:
    """Starts the chromedriver server on the CrOS device."""
    self._remote_chromedriver_server_process = self._ssh.start_remote_process(
        ' '.join([
            constants.CHROME_DRIVER_EXE_PATH,
            '--whitelisted-ips',  # Allow remote connections.
            f'--port={self._chromedriver_server_port}',
            '--verbose',
            f'--log-path={constants.CHROME_DRIVER_LOG}',
        ])
    )

    @retry.retry(
        exceptions=NotExpectedValueError,
        tries=3,
        delay=1,
        max_delay=3,
        backoff=1.3,
    )
    @verify_result(True)
    def wait_remote_chromedriver_starts() -> bool:
      return self._is_chromedriver_server_running()

    wait_remote_chromedriver_starts()
    self._log.debug('The remote chromedriver server started.')

  def _stop_remote_chromedriver_server(self) -> None:
    """Stops the chromedriver server on the CrOS device."""
    if self._remote_chromedriver_server_process is None:
      return

    @retry.retry(
        exceptions=NotExpectedValueError,
        tries=3,
        delay=1,
        max_delay=3,
        backoff=1.3,
    )
    @verify_result(False)
    def wait_remote_chromedriver_stops() -> bool:
      self._send_request_to_chromedriver('/shutdown')
      return self._is_chromedriver_server_running()

    wait_remote_chromedriver_stops()
    self._remote_chromedriver_server_process.wait(ignore_error=True)
    self._remote_chromedriver_server_process = None
    self._log.debug('The remote chromedriver server stopped.')

  def _get_remote_chrome_debugging_port(self) -> None:
    """Returns the remote debugging port for Chrome.

    Parse chrome process's command line argument to get the remote debugging
    port. if it is 0, look at DevToolsActivePort for the ephemeral port.

    Raises:
      Error: if fail to find or parse the command of the chrome process.
    """
    pid, command = unix_utils.get_oldest_by_name(
        self._ssh.execute_command,
        'chrome',
    )
    if command is None:
      raise Error('Fail to find the oldest "chrome" process.')

    matches = re.search('--remote-debugging-port=([0-9]+)', command)
    if not matches:
      raise Error(
          'Fail to find the "--remote-debugging-port" argument '
          f'from the "chrome" process, pid: {pid}, command: {command}'
      )

    port = int(matches.group(1))
    if port:
      self._remote_chrome_debugging_port = port
    else:
      dev_tool_active_port_str = self._ssh.get_remote_file_contents(
          f'{constants.USER_DATA_LOCATION}/DevToolsActivePort'
      ).split('\n')[0]
      self._remote_chrome_debugging_port = int(dev_tool_active_port_str)

  def _clear_remote_chrome_debugging_port(self) -> None:
    """Clears the attributes set in `_get_remote_chrome_debugging_port`."""
    self._remote_chrome_debugging_port = None

  def _build_webdriver(self) -> selenium_webdriver.Remote:
    """Builds the remote webdriver instance.

    Returns:
      The remote webdriver instance.
    """
    # Chrome must be already started before create the webdriver instance.
    self._open_a_new_chrome_tab()

    options = selenium_webdriver.ChromeOptions()
    options.debugger_address = f'localhost:{self._remote_chrome_debugging_port}'

    return _WebDrvierRemote(
        command_executor=(
            f'http://127.0.0.1:{self._local_forwarded_chromedriver_port}'
        ),
        desired_capabilities=options.to_capabilities(),
    )

  def _open_a_new_chrome_tab(self) -> None:
    # Note that the process listening on the debug port only accepts traffic
    # from localhost, so here we use SSH commands instead of sending HTTP
    # requests like `_send_request_to_chromedriver`.
    request_url = (
        f'http://localhost:{self._remote_chrome_debugging_port}/json/new'
    )
    command = f'curl -X PUT {request_url}'
    response = self._ssh.execute_command(command)
    self._log.debug(
        'Got output of the command to open a new Chrome tab: %s', response
    )

  def _stop_webdriver(self) -> None:
    """Stops the remote webdriver instance."""
    if self._webdriver is None:
      return

    # Closes the current tab.
    try:
      self._webdriver.close()
    except selenium_exceptions.WebDriverException:
      self._log.exception(
          'Ignoring the error caused by webdriver.close(). This is likely '
          'because the tab has already been closed.'
      )

    # Quits the instance of web driver.
    self._webdriver.quit()
    self._webdriver = None

  def _validate_webdriver_setup(self) -> None:
    """Validates webdriver has been setup properly."""
    if self._webdriver is None:
      raise WebDriverSetupError('The webdriver instance must not be None.')

    if self._webdriver.current_url == _WEBDRIVER_SETUP_FAIL_URL:
      raise WebDriverSetupError(
          'The webdriver is in abnormal state after steup, please stop and '
          'restart webdriver to recover.'
      )

  def _is_chromedriver_server_running(self) -> bool:
    """Whether the chromedriver server is up and running on the CrOS device.

    Returns:
      True if chromedriver server is up and running else False.
    """
    if self._remote_chromedriver_server_process is None:
      return False

    return self._send_request_to_chromedriver('/status') is not None

  def _send_request_to_chromedriver(self, request: str) -> Optional[str]:
    """Sends a request to the chromedriver server.

    Args:
      request: The target URL to send this request.

    Returns:
      A string represents the response of this request.
    """
    chromedriver_server_request_url = (
        f'http://localhost:{self._local_forwarded_chromedriver_port}{request}'
    )
    self._log.debug(
        'Sending request %s to chromedriver server, url: %s',
        request,
        chromedriver_server_request_url,
    )

    try:
      with urllib.request.urlopen(chromedriver_server_request_url) as response:
        response_str = response.read().decode('utf-8')
        self._log.debug('response to request %s: %s', request, response_str)
        return response_str
    except (urllib.error.URLError, http.client.RemoteDisconnected):
      return None

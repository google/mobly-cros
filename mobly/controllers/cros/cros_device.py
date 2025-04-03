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

"""Mobly controller module for a ChromeOS device."""

from __future__ import annotations

from collections.abc import Generator, Iterable, Sequence
import contextlib
import dataclasses
import logging
import os
import pathlib
import time
from typing import Any, Optional, TYPE_CHECKING

from mobly import logger as mobly_logger
from mobly import signals
from mobly import utils
import paramiko

from mobly.controllers.cros import cros_device_config
from mobly.controllers.cros.lib import build_info
from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import device_utils
from mobly.controllers.cros.lib import ssh as ssh_lib
from mobly.controllers.cros.lib import tast_client
from mobly.controllers.cros.lib import tast_service_manager

if TYPE_CHECKING:
  # pytype: disable=import-error
  # pylint: disable=g-bad-import-order, g-import-not-at-top
  from selenium import webdriver as selenium_webdriver
  # pylint: enable=g-bad-import-order, g-import-not-at-top
  # pytype: enable=import-error

_SSH_KEY_IDENTITY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'data/testing_rsa'
)

# This is used in the config file located in the test lab's home directory.
MOBLY_CONTROLLER_CONFIG_NAME = 'CrosDevice'

# Abbreviations for common use type
_BuildInfo = build_info.BuildInfo
_CrosDeviceConfig = cros_device_config.CrosDeviceConfig

_CROS_DEVICE_EMPTY_CONFIG_MSG = 'Configuration is empty, abort!'
_CROS_DEVICE_CONFIGS_NOT_LIST_MSG = (
    'Configurations should be a list of dicts, abort!'
)
_CROS_DEVICE_CONFIG_NOT_DICT_MSG = (
    'Each configuration for a ChromeOS device should be a dict, abort!'
)


class Error(signals.ControllerError):
  """Raised for errors related to the Chrome OS controller module."""


class DeviceError(Error):
  """Raised for errors specific to a CrosDevice object."""


class ServiceError(DeviceError):
  """Raised for errors specific to a CrosDevice service.

  A service is inherently associated with a device instance, so the service
  error type is a subtype of `DeviceError`.
  """


def create(configs: Iterable[dict[str, Any]]) -> Iterable[CrosDevice]:
  """Creates CrosDevice objects.

  Mobly uses this to instantiate CrosDevice controller objects from configs. The
  configs come from Mobly configs that look like:

    ```config.yaml
    TestBeds:
    - Name: SampleTestBed
      Controllers:
        CrosDevice:
        - hostname: 172.16.243.132
    ```

  Args:
    configs: a list of dicts, each representing a configuration for a ChromeOS
      device.

  Returns:
    A list of CrosDevice objects.

  Raises:
    Error: Invalid controller configs are given.
  """
  if not configs:
    raise Error(_CROS_DEVICE_EMPTY_CONFIG_MSG)
  elif not isinstance(configs, list):
    raise Error(f'{_CROS_DEVICE_CONFIGS_NOT_LIST_MSG}: {configs}')

  try:
    os.chmod(_SSH_KEY_IDENTITY, 0o600)
  except OSError as e:
    logging.warning('Failed to chmod %s: %s', _SSH_KEY_IDENTITY, e)

  crosds = []
  for config in configs:
    if not isinstance(config, dict):
      raise Error(f'{_CROS_DEVICE_CONFIG_NOT_DICT_MSG}: {config}')

    logging.debug('Creating CrosDevice from config: %s', config)
    try:
      crosd_config = _CrosDeviceConfig.from_dict(config)
      logging.debug('Created CrosDeviceConfig: %s', crosd_config)
    except cros_device_config.Error as err:
      raise Error(str(err)) from err

    crosds.append(CrosDevice(crosd_config))

  _remove_rootfs_verification_on_crosds(crosds)

  return crosds


def _remove_rootfs_verification_on_crosds(crosds: Iterable[CrosDevice]) -> None:
  """Removes root filesystem verification on CrOS devices if needed.

  This will ignore any error raised in the removal process, because it only
  results in missing some device logs.

  Args:
    crosds: The CrOS device controllers.
  """
  for crosd in crosds:
    if crosd.config.remove_rootfs_verification:
      try:
        device_utils.remove_rootfs_verification_if_not(crosd)
      except Exception:  # pylint: disable=broad-except
        crosd.log.exception(
            'Failed to remove root filesystem verification, some device '
            'logs may be missing.'
        )


def destroy(crosds: Iterable[CrosDevice]) -> None:
  """Destroys CrosDevice objects.

  Mobly uses this to destroy CrosDevice controller objects created by `create`.

  Args:
    crosds: list of CrosDevice.
  """
  for crosd in crosds:
    try:
      crosd.teardown()
    except Exception:  # pylint: disable=broad-except
      logging.exception('Failed to clean up properly.')


def get_info(devices: Sequence[CrosDevice]) -> Sequence[dict[str, Any]]:
  """Gets info from the CrosDevice objects used in a test run.

  Args:
    devices: A list of CrosDevice objects.

  Returns:
    A list of dict, each representing info for a CrOS device.
  """
  return [d.device_info for d in devices]


class CrosDevice:
  """Mobly controller for a ChromeOS device with test image.

  A ChromeOS test image has additional test-specific packages (ex: tast bundle
  executable, autotest lib) and also accepts incoming ssh connections with user
  root. More details can be found at:
  https://chromium.googlesource.com/chromiumos/docs/+/HEAD/developer_guide.md

  Attributes:
    ssh: the underlying SSH client object.
    hostname: the IP address of the ChromeOS device.
    config: The configurations for the ChromeOS device.
    ssh_port: the port of the ChromeOS device.
    ssh_forward_port: the port on the local machine for ssh port forwarding.
    gaia_email: the username to log the ChromeOS device in.
    gaia_password: the password to log the ChromeOS device in.
    serial: a string that identify the ChromeOS device.
    log_path: A string that is the path where all logs collected on this
      ChromeOS device should be stored.
    debug_tag: A string that represents this ChromeOS device in the debug info.
    log: A logger adapted from root logger with an added prefix specific to a
      remote test machine. The prefix is "[CrosDevice|<hostname>:<ssh_port>] ".
    webdriver: The remote webdriver for the ChromeOS device.
    tast_client: The Tast client object used for communicating with the Tast
      server.
    services: The object for users to call Tast services and managing the life
      cycles of Tast services.
  """

  _DEFAULT_LOGS_DIRECTORY = '/tmp/logs'

  # Timeout to wait for boot completion
  BOOT_COMPLETION_TIMEOUT_SECONDS = 5 * 60

  # Timeout to wait for ssh connection.
  SSH_CONNECT_TIMEOUT_SECONDS = None

  # Timeout to wait for banner to be presented.
  SSH_BANNER_TIMEOUT_SECONDS = None

  # Class variable annotations.
  log: mobly_logger.PrefixLoggerAdapter
  services: tast_service_manager.TastServiceManager

  def __init__(self, config: _CrosDeviceConfig) -> None:
    self._build_info = None
    self._model = None
    self._ssh = None
    self._webdriver_manager = None
    self.config = config
    self.hostname = config.hostname
    self.ssh_port = config.custom_ssh_port
    self.ssh_forward_port = config.custom_ssh_forward_port
    self._ssh_username = config.custom_ssh_username
    self._ssh_password = config.custom_ssh_password
    self.gaia_email = config.gaia_email
    self.gaia_password = config.gaia_password
    self.serial = f'{self.hostname}:{self.ssh_port}'

    # logging.log_path only exists when this is used within a Mobly test class.
    log_path = getattr(logging, 'log_path', self._DEFAULT_LOGS_DIRECTORY)
    log_filename = mobly_logger.sanitize_filename(f'CrosDevice_{self.serial}')
    self.log_path = os.path.join(log_path, log_filename)
    utils.create_dir(self.log_path)
    self.log = mobly_logger.PrefixLoggerAdapter(
        logging.getLogger(),
        {
            mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX: (
                f'[CrosDevice|{self.serial}]'
            )
        },
    )
    self._debug_tag = self.serial

    self.services = tast_service_manager.TastServiceManager(device=self)

  @property
  def debug_tag(self) -> str:
    """A string that represents this device in the debug info.

    This will be used as part of the prefix of debugging messages emitted by
    this device object, like log lines and the message of DeviceError. Default
    value is the device serial.
    """
    return self._debug_tag

  @debug_tag.setter
  def debug_tag(self, tag: str) -> None:
    """Setter for the debug tag."""
    self.log.info('Setting logging debug tag to "%s"', tag)
    self.log.set_log_prefix(f'[CrosDevice|{tag}]')
    self._debug_tag = tag

  def __repr__(self) -> str:
    return f'<CrosDevice|{self.debug_tag}>'

  @property
  def ssh(self) -> ssh_lib.SSHProxy:
    """The ssh connection to the ChromeOS device.

    Raises:
      paramiko.ssh_exception.BadHostKeyException: if the server’s host key
      could not be verified.
      paramiko.ssh_exception.AuthenticationException: if authentication failed.
      paramiko.ssh_exception.SSHException: if there was any other error
      connecting or establishing an SSH session.
      socket.error: if a socket error occurred while connecting.
    """
    if self._ssh is None:
      ssh_connection = self._create_ssh_connection()
      ssh_connection.connect(
          self.SSH_CONNECT_TIMEOUT_SECONDS, self.SSH_BANNER_TIMEOUT_SECONDS
      )
      self._ssh = ssh_connection
    return self._ssh

  def _create_ssh_connection(self) -> ssh_lib.SSHProxy:
    """Creates a new ssh connection to the ChromeOS device."""
    return ssh_lib.SSHProxy(
        hostname=self.hostname,
        ssh_port=self.ssh_port,
        username=self._ssh_username,
        password=self._ssh_password,
        keyfile=_SSH_KEY_IDENTITY if self._ssh_password is None else None,
    )

  @property
  def webdriver(
      self,
  ) -> selenium_webdriver.Remote:
    """The remote webdriver for the ChromeOS device.

    Raises:
      DeviceError: if fail to find or parse the command of the chrome process.
    """
    if self._webdriver_manager is None:
      # pytype: disable=import-error
      from mobly.controllers.cros.lib import webdriver_manager  # pylint: disable=g-import-not-at-top
      # pytype: enable=import-error
      manager = webdriver_manager.WebDriverManager(
          self.ssh, self.log, self.ssh_forward_port
      )
      self._webdriver_manager = manager
      try:
        manager.setup()
      except webdriver_manager.Error as err:
        self._raise_device_error(str(err))
    assert self._webdriver_manager.webdriver is not None  # By manager.setup().
    return self._webdriver_manager.webdriver

  @property
  def build_info(self) -> _BuildInfo:
    """Gets the build info of this ChromeOS device.

    Returns:
      A BuildInfo dataclass from this ChromeOS device.

    Raises:
      ssh.RemotePathDoesNotExistError: Info file is not found on Chromebook.
      ssh.ExecuteCommandError: ssh command encounters an error.
    """
    if self._build_info is None:
      self._build_info = _BuildInfo.collect(self.ssh)
    return self._build_info

  @property
  def device_info(self) -> dict[str, Any]:
    """Information to be pulled into controller info in the test summary file.

    The serial, model and build_info are included.
    """
    info = {
        'serial': self.serial,
        'model': self.model,
        'build_info': dataclasses.asdict(self.build_info),
        'is_virtual': self.is_virtual,
    }
    return info

  @property
  def model(self) -> str:
    """The model name for the device."""
    if self._model is None:
      self._model = self.ssh.execute_command('cros_config / name')
    return self._model

  @property
  def is_virtual(self) -> bool:
    """Whether the device is a virtual device."""
    return bool(
        self.ssh.execute_command('grep hypervisor /proc/cpuinfo || echo -n')
    )

  @property
  def tast_client(self) -> tast_client.TastClient:
    """The Tast client object used for communicating with the Tast server."""
    return self.services.tast_client

  @contextlib.contextmanager
  def handle_reboot(self) -> Generator[None, None, None]:
    """Handles the rebooting process.

    The device can temporarily lose ssh connection due to user-triggered
    reboot.

    For sample usage, see self.reboot().

    Yields:
      The context for user to trigger device reboot.

    Raises:
      DeviceError: Raised if booting process timed out.
    """
    live_tast_services = self.services.list_live_services()
    self.services.stop_all()
    if self._webdriver_manager is not None:
      self._webdriver_manager.teardown()
      self._webdriver_manager = None
    try:
      yield
    finally:
      self._ssh = None
      self._wait_for_boot_completion()
      # On boot completion, invalidate the `build_info` cache since any
      # value it had from before boot completion is potentially invalid.
      self._build_info = None
      self.services.start_services(live_tast_services)

  def _wait_for_boot_completion(self) -> None:
    """Waits for a ssh connection can be reestablished.

    Raises:
      DeviceError: Raised if booting process timed out.
    """
    deadline = time.perf_counter() + self.BOOT_COMPLETION_TIMEOUT_SECONDS
    while time.perf_counter() < deadline:
      try:
        self.ssh.execute_command('echo')
        break
      except (
          paramiko.ssh_exception.NoValidConnectionsError,
          paramiko.ssh_exception.SSHException,
          ConnectionResetError,
          TimeoutError,
      ):
        # ssh connect may fail during certain period of booting
        # process, which is normal. Ignoring these errors.
        pass
      time.sleep(5)
    else:
      self._raise_device_error('Booting process timed out')

  def reboot(self) -> None:
    """Reboots the device.

    Generally one should use this method to reboot the device instead of
    directly calling `ssh.execute_command('sudo reboot')`. Because this method
    gracefully handles the teardown and restoration of running services.

    This method is blocking and only returns when the reboot has completed
    and the services restored.
    """
    self.log.info('Rebooting CrOS ...')
    with self.handle_reboot():
      # Use execute_command_async here to avoid getting stuck in dangling
      # ssh connection during rebooting.
      self.ssh.execute_command_async('sudo reboot')
      time.sleep(10)

  @contextlib.contextmanager
  def handle_system_suspend(self) -> Generator[None, None, None]:
    """Handles the system suspend process.

    The suspension operation is a CrOS system-wide suspension triggered by
    command `powerd_dbus_suspend`. This can be used to simulate sleep mode
    during tests. The suspension operation will destroy the states of running
    Tast services on the remote device, so this class will properly suspend
    and resume these services.

    For sample usage, see self.suspend().

    Yields:
      The context for users to trigger device suspension.
    """
    live_tast_services = self.services.list_live_services()
    self.services.suspend_all()
    try:
      yield
    finally:
      self.services.resume_services_from_suspension(live_tast_services)

  def suspend(self, suspend_for_sec: int) -> None:
    """Suspends the device.

    This method uses the command `powerd_dbus_suspend` to suspend the device.
    This can be used to simulate sleep mode during tests.

    Generally one should use this method to suspend the device instead of
    directly calling the suspend command `powerd_dbus_suspend`. Because this
    method gracefully handles the teardown and restoration of running services.

    This method is blocking and only returns when the suspension has completed
    and the services were restored.

    Args:
      suspend_for_sec: The time in seconds that the device will be suspended.
    """
    self.log.info('Suspending the device.')
    command = f'powerd_dbus_suspend --suspend_for_sec={suspend_for_sec}'
    with self.handle_system_suspend():
      self.ssh.execute_command(command)

  def take_screenshot(
      self, destination: Optional[str] = None, prefix: str = 'screenshot'
  ) -> pathlib.Path:
    """Takes a screenshot of the device.

    Args:
      destination: Full path to the directory to save in.
      prefix: Prefix file name of the screenshot.

    Returns:
      Full path to the screenshot file on the host.
    """
    timestamp = mobly_logger.get_log_file_timestamp()
    filename = f'{prefix},{self.serial},{self.build_info.board},{timestamp}.png'
    cros_path = pathlib.PurePosixPath('/tmp/', filename)
    self.ssh.execute_command(f'screenshot {cros_path}')
    if destination is None:
      destination = self.log_path
    else:
      utils.create_dir(destination)
    host_path = pathlib.Path(destination, filename)
    self.ssh.pull(
        remote_src_filepath=str(cros_path), local_dest_filepath=str(host_path)
    )
    self.ssh.rm_file(str(cros_path))
    self.log.debug('Screenshot taken, saved on the host: %s', host_path)
    return host_path

  def input_text(self, text: str) -> None:
    """Inputs text on the test device by simulating typing on the keyboard.

    The text is a case-sensitive string. The left Shift key is automatically
    pressed and released when inputting the characters that need the Shift key.

    This uses the Tast gRPC service KeyboardService to simulate typing on the
    keyboard. More details about the supported characters and requirements per:
    http://chromium.googlesource.com/chromiumos/platform/tast-tests/+/refs/heads/main/src/go.chromium.org/tast-tests/cros/services/cros/inputs/keyboard_service.proto

    Args:
      text: The string to be inputted on the test device.
    """
    self.services.keyboard_service_wrapper.type(text)

  def input_hotkey(self, hotkey: str) -> None:
    """Inputs the hotkey by simulating key events on the keyboard.

    The hotkey is described as a sequence of '+'-separated, case-insensitive key
    characters. In addition to English letters, the following key names can be
    used:

    * Modifiers: "Ctrl", "Alt", "Search", "Shift".
    * Whitespace: "Enter", "Space", "Tab", "Backspace"
    * Function keys: "F1", "F2", ..., "F12"

    If needed, "Shift" key must be included in the hotkey, for example, use
    "Ctrl+Shift+/" rather than "Ctrl+?".

    This uses the Tast gRPC service KeyboardService to simulate key events on
    the keyboard. More details about the supported characters per:
    http://chromium.googlesource.com/chromiumos/platform/tast-tests/+/refs/heads/main/src/go.chromium.org/tast-tests/cros/services/cros/inputs/keyboard_service.proto

    Args:
      hotkey: The string describing the hotkey.
    """
    self.services.keyboard_service_wrapper.accel(hotkey)

  def teardown(self):
    """Tears CrosDevice object down."""
    if self._webdriver_manager:
      self._webdriver_manager.teardown()
      self._webdriver_manager = None

    self.services.unregister_all()

    if self._ssh:
      # Closes the SSH session.
      self._ssh.disconnect()
      self._ssh = None

  def _raise_device_error(self, msg: str) -> None:
    raise DeviceError(f'{repr(self)} {msg}')

  def _raise_service_error(self, service_type: str, msg: str) -> None:
    raise ServiceError(f'Service<{service_type}> {msg}')

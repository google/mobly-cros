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

"""The service to manage a Tast session on a CrOS device."""

from collections.abc import Sequence
import dataclasses
import time
import typing
from typing import Any, Optional, cast

import grpc
from mobly import logger as mobly_logger
from mobly.controllers.android_device_lib import errors
from mobly.controllers.android_device_lib.services import base_service
from mobly.snippet import errors as mobly_snippet_errors

from google.protobuf import empty_pb2
from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import ssh
from mobly.controllers.cros.lib import tast_client
from tast.cros.services.cros.policy import policy_pb2
from tast.cros.services.cros.policy import policy_pb2_grpc
from tast.cros.services.cros.ui import chrome_service_pb2
from tast.cros.services.cros.ui import chrome_service_pb2_grpc

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any

# Aliases for Login modes
LOGIN_MODE_UNSPECIFIED = chrome_service_pb2.LoginMode.LOGIN_MODE_UNSPECIFIED
LOGIN_MODE_FAKE_LOGIN = chrome_service_pb2.LoginMode.LOGIN_MODE_FAKE_LOGIN
LOGIN_MODE_GAIA_LOGIN = chrome_service_pb2.LoginMode.LOGIN_MODE_GAIA_LOGIN
LOGIN_MODE_GUEST_LOGIN = chrome_service_pb2.LoginMode.LOGIN_MODE_GUEST_LOGIN

# Constants for the DMServer Environments. go/dmserver-envs
DM_SERVER_ALPHA_URL = (
    'https://crosman-alpha.sandbox.google.com/devicemanagement/data/api'
)
DM_SERVER_STAGING_URL = (
    'https://crosman-staging.sandbox.google.com/devicemanagement/data/api'
)
DM_SERVER_PROD_URL = 'https://m.google.com/devicemanagement/data/api'

# The error message of login failures caused by wrong password.
LOGIN_FAIL_MESSAGE_WRONG_PASSWORD = (
    'failed to wait for user mount and validate type'
)


class ConfigError(Exception):
  """Raised when received an invalid config."""


class TastSessionServiceError(errors.ServiceError):
  """Base error type for Tast session service."""

  SERVICE_TYPE = 'TastSession'


class TastServerNotRunningError(TastSessionServiceError):
  """Raised when this service is running while Tast server has died."""


@dataclasses.dataclass
class Config:
  """A configuration object for configuring the Tast session service.

  Attributes:
    login_mode: The mode for user login. GAIA mode uses GAIA backend to verify
      the login credential, which can be slow and sometimes flaky. If your test
      doesn't require GAIA login, you can use fake mode which logs in with the
      given account without verifying password. The default mode is actually
      fake mode plus default test account. Full list and information for login
      modes per:
      http://chromium.googlesource.com/chromiumos/platform/tast-tests/+/refs/heads/main/src/go.chromium.org/tast-tests/cros/services/cros/ui/chrome_service.proto
    username: The name of the user account to login, typically it is a gmail
      address.
    password: The password of the user account to login.
    try_reuse_session: True for trying to reuse the current session. False for
      always starting a new session.
    keep_state: True for keeping existing user profiles. False for wiping these
      profiles before login. Generally `keep_state=False` should only be used at
      the beginning of the test and clears the device data. Therefore, after the
      Tast session service is started for the first time, the Tast session
      service will modify this parameter to True to ensure that the data on the
      device will not be cleared when the service is restarted in the middle of
      the test.
    extra_args: Additional runtime arguments to pass to Chrome.
    enable_features: The Chrome features to enable when starting a new session.
      The function of this field is similar to enabling them through
      chrome://flags.
    disable_features: The Chrome features to disable when starting a new
      session. The function of this field is similar to disabling them through
      chrome://flags.
    region: The region of the session to start. This will determine the system
      language.
    login_mode_name: A string for the login mode name used for logging.
    gaia_enroll_and_login: True if doing device enroll and login with GAIA
      account. Only username, password, and dm_server_url are needed if this
      flag is on.
    dm_server_url: The DM Server URL used for device enrollment.
  """

  login_mode: chrome_service_pb2.LoginMode = LOGIN_MODE_UNSPECIFIED
  username: Optional[str] = None
  password: Optional[str] = None
  try_reuse_session: bool = False
  keep_state: bool = True
  extra_args: Sequence[str] = dataclasses.field(default_factory=list)
  enable_features: Sequence[str] = dataclasses.field(default_factory=list)
  disable_features: Sequence[str] = dataclasses.field(default_factory=list)
  region: str = 'us'
  gaia_enroll_and_login: bool = False
  dm_server_url: str = DM_SERVER_PROD_URL

  @property
  def login_mode_name(self) -> str:
    """A string for the login mode name used for logging."""
    if self.gaia_enroll_and_login:
      return 'GAIA_ENROLL_AND_LOGIN'
    return chrome_service_pb2.LoginMode.Name(self.login_mode)

  def __post_init__(self) -> None:
    self._check_login_credential_validity()

  def _check_login_credential_validity(self) -> None:
    """Checks the validity of the login credential.

    If gaia_enroll_and_login is True, check that username, password, and
    dm_server_url are set.

    If gaia_enroll_and_login is False, do the following checks:
    * For login mode default and guest, users should not set username and
      password. The guest mode doesn't require an account. For the default
      mode, the Tast service will ignore the username and password, and use
      the default account for login.
    * For login mode FAKE and GAIA, users must set username and password.

    Raises:
      ConfigError: If the given login credential is invalid.
    """
    if self.gaia_enroll_and_login:

      if not self.username:
        raise ConfigError(
            f'Username should be set for {self.login_mode_name}, but found '
            f'username={self.username}'
        )

      if not self.password:
        raise ConfigError(
            f'Password should be set for {self.login_mode_name}, but found '
            f'password={self.password}'
        )

      if not self.dm_server_url:
        raise ConfigError(
            f'DM Server URL should be set for {self.login_mode_name}, but '
            f'found dm_server_url={self.dm_server_url}'
        )
      return

    if self.login_mode in (LOGIN_MODE_UNSPECIFIED, LOGIN_MODE_GUEST_LOGIN):

      if self.username is not None:
        raise ConfigError(
            f'Username should not be set for {self.login_mode_name}, but found '
            f'username={self.username}')

      if self.password is not None:
        raise ConfigError(
            f'Password should not be set for {self.login_mode_name}, but found '
            f'password={self.password}')

    if self.login_mode in (LOGIN_MODE_FAKE_LOGIN, LOGIN_MODE_GAIA_LOGIN):

      if self.username is None:
        raise ConfigError(
            f'Username should be set for {self.login_mode_name}, but found '
            f'username={self.username}')

      if self.password is None:
        raise ConfigError(
            f'Password should be set for {self.login_mode_name}, but found '
            f'password={self.password}')

  def generate_login_grpc_request(self) -> chrome_service_pb2.NewRequest:
    """Generates the gRPC request message used for login."""
    return chrome_service_pb2.NewRequest(
        login_mode=self.login_mode,
        credentials=chrome_service_pb2.NewRequest.Credentials(
            username=self.username,
            password=self.password,
        ),
        try_reuse_session=self.try_reuse_session,
        keep_state=self.keep_state,
        extra_args=self.extra_args,
        enable_features=self.enable_features,
        disable_features=self.disable_features,
        region=self.region,
    )

  def generate_enroll_and_login_grpc_request(
      self,
  ) -> policy_pb2.GAIAEnrollAndLoginUsingChromeRequest:
    """Generates the gRPC request message used for GAIAEnrollAndLogin."""
    return policy_pb2.GAIAEnrollAndLoginUsingChromeRequest(
        username=self.username,
        password=self.password,
        dmserverURL=self.dm_server_url,
    )


class TastSessionService(base_service.BaseService):
  """A service for managing the Tast Chrome session.

  From a user's point of view:
  * This service conducts the login operation on CrOS device.
  * Please register this service before registering any other Tast service.

  Under the hook, this service creates a new Tast session on the Tast server,
  and manages the lifecycle of the session. Most Tast services rely on
  this session for their functionality, like triggering UI automation and
  recording screen.

  This service depends on the Tast gRPC service `ChromeService` and uses the
  Tast client to interact with `ChromeService`. If device enrollment is
  needed, this service instead communicates with the Tast gRPC service
  "PolicyService" to do GAIA enroll and login.

  Attributes:
    log: A logger adapted from the CrOS device logger, which adds the identifier
      '[TastSessionService]' to each log line: '<CrosDevice log prefix>
      [TastSessionService] <message>'.
  """

  def __init__(self,
               device: 'CrosDevice',
               configs: Optional[Config] = None) -> None:
    """Initializes the instance of Tast session service.

    Args:
      device: The CrOS device controller object.
      configs: The configuration parameters for the Tast session service.
    """
    configs = configs if configs is not None else Config()
    super().__init__(device, configs)
    self._tast_client: tast_client.TastClient = device.tast_client
    self.log = mobly_logger.PrefixLoggerAdapter(
        self._device.log,
        {
            mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX:
                '[TastSessionService]'
        },
    )
    self._is_alive = False

  @property
  def is_alive(self) -> bool:
    """True if the Tast session service is alive; False otherwise."""
    if self._is_alive:
      # Raise error if this service is alive but Tast server died.
      self._assert_tast_server_alive()

    return self._is_alive

  def _get_grpc_chrome_service_stub(
      self,
  ) -> chrome_service_pb2_grpc.ChromeServiceStub:
    stub = self._tast_client.get_or_create_grpc_stub(
        tast_client.TAST_CHROME_SERVICE_NAME)
    return typing.cast(chrome_service_pb2_grpc.ChromeServiceStub, stub)

  def _get_grpc_policy_service_stub(self) -> policy_pb2_grpc.PolicyServiceStub:
    stub = self._tast_client.get_or_create_grpc_stub(
        tast_client.TAST_POLICY_SERVICE_NAME
    )
    return typing.cast(policy_pb2_grpc.PolicyServiceStub, stub)

  def start(self) -> None:
    """Starts a new Tast session and logs in with the account in config."""
    self._assert_tast_server_alive()

    if self._configs.gaia_enroll_and_login:
      request = self._configs.generate_enroll_and_login_grpc_request()
      service_name = 'PolicyService'
    else:
      request = self._configs.generate_login_grpc_request()
      service_name = 'ChromeService'
    # This process can be slow, thus we use log.info to inform people what
    # actions we are performing
    self.log.info(
        'Trying to create a new Tast session through Tast gRPC service %s.',
        service_name,
    )

    self.log.debug('Creating a new Tast session with request: %s', request)
    try:
      if self._configs.gaia_enroll_and_login:
        response = (
            self._get_grpc_policy_service_stub().GAIAEnrollAndLoginUsingChrome(
                request, timeout=constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC
            )
        )
      else:
        response = self._get_grpc_chrome_service_stub().New(
            request, timeout=constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC
        )
      self.log.debug('Created Tast session with response: %s', response)
    except grpc.RpcError as e:
      self.log.debug('Taking a screenshot when login failed.')
      # When the login fails, it needs to wait several seconds for the UI to
      # be stable before taking a screenshot
      time.sleep(3)
      try:
        self._device.take_screenshot(prefix='screenshot_when_login_failed')
        self.log.info(
            'Login failed because of an RPC Error, please check the device log '
            'and screenshot for debugging.'
        )
      except ssh.ExecuteCommandError:
        self.log.debug('Ignoring the screenshot error.')

      # See (internal) for why we need cast here.
      error = cast(grpc.Call, e)
      if (
          self._configs.login_mode == LOGIN_MODE_GAIA_LOGIN
          and LOGIN_FAIL_MESSAGE_WRONG_PASSWORD in error.details()
      ):
        raise TastSessionServiceError(
            self._device,
            'Failed to login on the CrOS due to user mount failure. Please '
            'check if you are using the correct OTA account and password.',
        ) from e
      raise

    self._is_alive = True

    # We should set keep_state to True because it should only be set to False
    # for the first time starting a Tast session.
    self._set_keep_state_to_true_after_startup()

  def _set_keep_state_to_true_after_startup(self):
    if not self._configs.keep_state:
      self._configs.keep_state = True

  def stop(self) -> None:
    """Stops the current Tast session."""
    if not self.is_alive:
      return

    request = empty_pb2.Empty()
    self.log.debug('Closing the created Tast session with request: %s', request)
    if self._configs.gaia_enroll_and_login:
      response = self._get_grpc_policy_service_stub().Logout(
          request, timeout=constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC
      )
    else:
      response = self._get_grpc_chrome_service_stub().Close(
          request, timeout=constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC
      )
    self.log.debug('Tast session closed with response: %s', response)
    self._is_alive = False

  def _assert_tast_server_alive(self):
    """Asserts that the Tast server is alive.

    Raises:
      TastServerNotRunningError: If the Tast server has died.
    """
    try:
      self._tast_client.check_server_proc_running()
    except mobly_snippet_errors.ServerDiedError as e:
      raise TastServerNotRunningError(
          self._device, 'Tast Server process has died unexpectedly.') from e

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

"""The module to manage Tast services and provide user interfaces.

Example Usage:

.. code-block:: python

  # Test setUp phase
  # =========================================================
  tast_service_manager = TastServiceManager(cros_device)

  # Register the Tast session service before registering any other services.
  # This step will login into a user session on the CrOS device.
  login_config = tast_session_service.Config(
      username=TEST_USER,
      password=TEST_PASSWORD,
      login_mode=tast_session_service.LOGIN_MODE_FAKE_LOGIN,
  )
  tast_service_manager.register(
      'tast_session_service',
      tast_session_service.TastSessionService,
      configs=login_config,
  )

  # Register the screen recorder service
  tast_service_manager.register(
      'screen_recorder_service',
      screen_recorder_service.ScreenRecorderService)

  # During a test
  # =========================================================
  # Use the keyboard service to type
  tast_service_manager.keyboard_service_wrapper.type('hello world')

  # Test Teardown phase
  # =========================================================
  tast_service_manager.create_output_excerpts_all(current_test_info)

  # When destroying the cros_device
  # =========================================================
  tast_service_manager.unregister_all()
"""

import collections
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from mobly import expects
from mobly import logger as mobly_logger
from mobly.controllers.android_device_lib import service_manager
from mobly.controllers.android_device_lib.services import base_service

from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import tast_client
from mobly.controllers.cros.lib import tast_service_wrapper
from mobly.controllers.cros.lib.tast_services import device_log_service
from mobly.controllers.cros.lib.tast_services import floss_pandora_service
from mobly.controllers.cros.lib.tast_services import tast_session_service

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any

# Type aliases
_P = ParamSpec('_P')
_T = TypeVar('_T')
_FuncSignature = Callable[_P, _T]


# The service class supported to use in this tast service manager
_SUPPORTED_SERVICE_CLASS = [
    tast_session_service.TastSessionService,
    device_log_service.DeviceLogService,
    floss_pandora_service.FlossPandoraService,
]

# The service classes that can only be used when Tast Session Service is running
_SERVICE_CLASSES_WITH_TAST_SESSION_SERVICE_DENPENDENCY = [
]

# TODO:  Remove this try-except block once we have a
# service manager for CrOS services.
# Handle dynamically importing the screen service dependency for now.
try:
  # pytype: disable=import-error
  from mobly.controllers.cros.lib.tast_services import screen_recorder_service  # pylint: disable=g-import-not-at-top
  # pytype: enable=import-error
  _SUPPORTED_SERVICE_CLASS.append(screen_recorder_service.ScreenRecorderService)
  _SERVICE_CLASSES_WITH_TAST_SESSION_SERVICE_DENPENDENCY.append(
      screen_recorder_service.ScreenRecorderService
  )
except ImportError:
  # Silently ignore the import error.
  pass


class Error(Exception):
  """Base error type for this module."""

  def __init__(self, device: 'CrosDevice', message: str) -> None:
    super().__init__(f'{repr(device)} {message}')


class MissingTastSessionError(Error):
  """Error for starting any other service before Tast session service."""


class TastSessionIsInUseError(Error):
  """Error for stopping the Tast session service before other services."""


class InvalidCrosDeviceObjectError(Error):
  """Error when got an invalid CrOS device object."""


def assert_tast_session_service_alive(func: _FuncSignature) -> _FuncSignature:
  """Asserts that Tast Session Service is alive.

  This is used as a decorator and has the following implicit assumptions on the
  decorated function:

  * The first argument `device` of the decorated function is a CrOS device.
  * The `device.services` is a Tast service manager instance.

  Args:
    func: The function to be decorated.

  Returns:
    The decorated function.
  """

  def wrapper(device: 'CrosDevice', *args, **kwargs):
    if not isinstance(device.services, TastServiceManager):
      raise InvalidCrosDeviceObjectError(
          device,
          'device.services must be a TastServiceManager instance, but got:'
          f' {type(device.services)}',
      )

    if not device.services.is_tast_session_service_alive():
      raise MissingTastSessionError(
          device,
          'The Tast session service is required while it is not alive.',
      )

    return func(device, *args, **kwargs)

  return wrapper


def _is_tast_session_service(service_obj: base_service.BaseService) -> bool:
  """True if the object is a TastSessionService instance; False otherwise."""
  return isinstance(service_obj, tast_session_service.TastSessionService)


def _has_tast_session_service_dependency(
    service_obj: base_service.BaseService) -> bool:
  """True if the object has a TastSessionService dependency; False otherwise."""
  for service_class in _SERVICE_CLASSES_WITH_TAST_SESSION_SERVICE_DENPENDENCY:
    if isinstance(service_obj, service_class):
      return True
  return False


def _assert_not_conflict_with_reserved_service_aliases(
    device: 'CrosDevice',
    alias: str,
    service_class: type[base_service.BaseService],
) -> None:
  """Asserts that reserved service aliases are not used by other services."""
  # Alias 'snippets' is reserved for SnippetManagementService and should not
  # be used by other services.

  if alias == constants.SNIPPET_MANAGEMENT_SERVICE_NAME:
    raise Error(
        device, f'Registering service class "{service_class}" with a reserved '
        f'alias "{alias}" is not allowed. Please use a different alias.')


class TastServiceManager(service_manager.ServiceManager):
  """The class to manage Tast services and provide user interfaces.

  This class inherits from the `service_manager` in Mobly android device
  library, and has following differences:

  * This class is only responsible for managing Tast-related components,
    including two Tast service classes, two wrapper classes of the Tast service
    and a Tast client.
  * This manager will check the dependencies between Tast components, i.e.
    `TastSessionService` must be started before using `ScreenRecorderService`
    and `AutomationServiceWrapper`.
  * For Tast services, each service class can only be registered once.
  """

  def __init__(self, device: 'CrosDevice') -> None:
    """Initializes a Tast service manager object.

    Args:
      device: The controller object for the CrOS device.
    """
    self._device = device
    self._tast_client = None
    self._service_objects: dict[
        str, base_service.BaseService] = collections.OrderedDict()
    self._keyboard_service_wrapper = None
    self._automation_service_wrapper = None
    self._log = mobly_logger.PrefixLoggerAdapter(
        device.log,
        {
            mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX:
                '[TastServiceManager]'
        },
    )

  def register(self,
               alias: str,
               service_class: type[base_service.BaseService],
               configs: Any = None,
               start_service: bool = True) -> None:
    """Registers a service.

    This will create a service instance, start the service, and add the instance
    to the manager. Before starting any other service, this will check that
    TastSessionService is started. Each service class can only be registered
    once.

    Args:
      alias: The alias representing the service class to instantiate.
      service_class: The service class to instantiate.
      configs: The config object to pass to the service class's constructor.
      start_service: True for starting the service. False otherwise.

    Raises:
      Error: If the given alias or the service class is invalid.
      MissingTastSessionError: If trying to start any other service before
        starting the Tast session service.
    """
    self._assert_valid_service_class(service_class)
    self._assert_service_class_is_not_registered(service_class)
    _assert_not_conflict_with_reserved_service_aliases(self._device, alias,
                                                       service_class)

    if self._service_objects.get(alias) is not None:
      raise Error(self._device,
                  f'A service is already registered with alias "{alias}".')

    service_obj = service_class(self._device, configs)
    service_obj.alias = alias

    if start_service:
      self._start_one_service_obj(service_obj)

    self._service_objects[alias] = service_obj

  def unregister(self, alias: str) -> None:
    """Unregisters the specified service instance.

    Stops a service and removes it from the manager.

    Args:
      alias: The alias of the service instance to unregister.

    Raises:
      Error: If failed to find the service with the given alias.
      TastSessionIsInUseError: If trying to stop the Tast session service while
        other services are alive.
    """
    if alias not in self._service_objects:
      raise Error(self._device,
                  f'No service is registered with alias "{alias}".')

    self._log.debug('Unregistering service %s', alias)
    service_obj = self._service_objects.pop(alias)
    self._stop_one_service_obj(service_obj)

  def start_services(self, service_aliases: list[str]) -> None:
    """Starts the specified services.

    Services will be started in the order specified by the input list.
    No-op for services that are already running.

    Args:
      service_aliases: The aliases of services to start.

    Raises:
      Error: If failed to find the service with the given alias.
      MissingTastSessionError: If trying to start any other service before
        starting the Tast session service.
    """
    for alias in service_aliases:
      if alias not in self._service_objects:
        raise Error(
            self._device,
            f'No service is registered under the name "{alias}", cannot start.')

      service_obj = self._service_objects[alias]
      self._start_one_service_obj(service_obj)

  def stop_all(self) -> None:
    """Stops all active service instances, service wrappers and the Tast client.

    Services will be stopped in the reverse order they were registered.
    """
    for service in reversed(self._service_objects.values()):
      self._stop_one_service_obj(service)

    self._stop_tast_client_and_service_wrappers()

  def unregister_all(self) -> None:
    """Safely unregisters all service instances, wrappers and the Tast client.

    Errors occurred here will be recorded but not raised.
    """
    aliases = list(reversed(self._service_objects.keys()))
    for alias in aliases:
      self.unregister(alias)

    self._stop_tast_client_and_service_wrappers()
    self._tast_client = None

  def unregister_tast_session_service(
      self, stop_tast_client: bool = False
  ) -> None:
    """Safely unregisters Tast Session Service and related components.

    The related components include service instances, wrappers that have
    dependencies on TastSessionService and the Tast client.

    Args:
      stop_tast_client: whether to stop the Tast client.
    """
    # Automation service wrapper also has dependency on Tast Session
    self._automation_service_wrapper = None

    aliases = list(reversed(self._service_objects.keys()))
    for alias in aliases:
      service_obj = self._service_objects.get(alias)
      if _is_tast_session_service(
          service_obj
      ) or _has_tast_session_service_dependency(service_obj):
        self.unregister(alias)

    if stop_tast_client:
      self._stop_tast_client_and_service_wrappers()
      self._tast_client = None

  def suspend_all(self) -> None:
    """Suspends all service instances.

    Services will be suspended in the reverse order they were registered.

    Regarding the specific implementation, this method will stop all the
    services. Note that this does not stop the tast client.
    """
    for service in reversed(self._service_objects.values()):
      self._stop_one_service_obj(service)

  def resume_services_from_suspension(self, service_aliases: list[str]) -> None:
    """Resumes services from suspension.

    Generally, this method is for resuming the services suspended by the method
    `suspend_all`. Services will be resumed in the order specified by the input
    list.

    Regarding the specific implementation, resuming these services is equivalent
    to starting them.

    Args:
      service_aliases: list of strings, the aliases of services to start.

    Raises:
      Error: If failed to find the service with the given alias.
    """
    for alias in service_aliases:
      if alias not in self._service_objects:
        raise Error(
            self._device,
            f'No service is registered under the name "{alias}", cannot resume.'
        )

      service_obj = self._service_objects[alias]
      self._start_one_service_obj(service_obj)

  def is_tast_session_service_alive(self) -> bool:
    """Returns True if the TastSessionService is alive; False otherwise."""

    def _is_live_tast_session_service(service):
      return _is_tast_session_service(service) and service.is_alive

    if not list(
        filter(_is_live_tast_session_service, self._service_objects.values())):
      return False

    return True

  @property
  def tast_client(self) -> tast_client.TastClient:
    """The Tast client object used for communicating with the Tast server."""
    self._start_tast_client_if_not_running()
    return self._tast_client

  @property
  def keyboard_service_wrapper(
      self) -> tast_service_wrapper.KeyboardServiceWrapper:
    """The wrapper for invoking RPC methods in Keyboard Service.

    When accessing this property, the Tast service manager will create the
    wrapper object if it does not exist.
    """
    if self._keyboard_service_wrapper is not None:
      return self._keyboard_service_wrapper

    self._start_tast_client_if_not_running()
    self._keyboard_service_wrapper = (
        tast_service_wrapper.KeyboardServiceWrapper(self._tast_client,
                                                    self._device.log))

    return self._keyboard_service_wrapper

  @property
  def automation_service_wrapper(
      self) -> tast_service_wrapper.AutomationServiceWrapper:
    """The wrapper for invoking RPC methods in Automation Service.

    When accessing this property, the Tast service manager will create the
    wrapper object if it does not exist.
    """
    if self._automation_service_wrapper is not None:
      return self._automation_service_wrapper

    self._assert_tast_session_service_alive(
        error_msg=('Using Tast Automation service before starting Tast '
                   'session service is forbidden.'))

    self._automation_service_wrapper = (
        tast_service_wrapper.AutomationServiceWrapper(self._tast_client,
                                                      self._device.log))
    return self._automation_service_wrapper

  def _start_one_service_obj(self,
                             service_obj: base_service.BaseService) -> None:
    """Starts the specified service object.

    If the given object has Tast session service dependency, this will check
    whether the Tast session service is alive.

    This will start the Tast client if Tast client is not alive.

    Args:
      service_obj: The service object to start.

    Raises:
      MissingTastSessionError: If trying to start any other service before
        starting the Tast session service.
    """
    if _has_tast_session_service_dependency(service_obj):
      error_msg = (f'Starting service {service_obj.alias} before Tast Session '
                   'service is forbidden.')
      self._assert_tast_session_service_alive(error_msg)

    self._start_tast_client_if_not_running()

    if not service_obj.is_alive:
      service_obj.start()

  def _assert_tast_session_service_alive(self, error_msg: str) -> None:
    """Asserts the Tast session service is alive."""

    if not self.is_tast_session_service_alive():
      raise MissingTastSessionError(self._device, error_msg)

  def _assert_valid_service_class(
      self, service_class: type[base_service.BaseService]) -> None:
    if service_class not in _SUPPORTED_SERVICE_CLASS:
      raise Error(
          self._device, f'Got invalid service class {service_class}. The '
          f'Supported classes are: {_SUPPORTED_SERVICE_CLASS}')

  def _assert_service_class_is_not_registered(
      self, service_class: type[base_service.BaseService]) -> None:
    """Asserts that the given service class is not registered."""
    service_objects = filter(
        lambda service_obj: isinstance(service_obj, service_class),
        self._service_objects.values())
    service_objects = list(service_objects)

    if service_objects:
      service_obj = service_objects[0]
      raise Error(
          self._device,
          'No service class can be registered more than once. Got service '
          f'class {service_class} which has been registered under name '
          f'"{service_obj.alias}".')

  def _start_tast_client_if_not_running(self) -> None:
    if self._tast_client is None:
      self._tast_client = tast_client.TastClient(self._device)

    if not self._tast_client.is_alive:
      self._tast_client.initialize()

  def _stop_one_service_obj(self,
                            service_obj: base_service.BaseService) -> None:
    """Stops the specified service object.

    If trying to stop the Tast session service while any alive service has
    Tast session service dependency, this will raise an error.

    Args:
      service_obj: The service object to stop.

    Raises:
      TastSessionIsInUseError: If trying to stop the Tast session service while
        other services are alive.
    """
    if _is_tast_session_service(service_obj):
      for temp_service in self._service_objects.values():
        if _has_tast_session_service_dependency(
            temp_service) and temp_service.is_alive:
          raise TastSessionIsInUseError(
              self._device,
              'It is forbidden to stop the Tast session service when service '
              f'"{temp_service.alias}" is alive.')

    if service_obj.is_alive:
      with expects.expect_no_raises(
          f'Failed to stop service instance "{service_obj.alias}".'):
        service_obj.stop()

  def _stop_tast_client_and_service_wrappers(self) -> None:
    """Stops the Tast client and service wrappers.

    Stopping the Tast client will throw an error if any of the services are
    alive.

    Raises:
      Error: If trying to stop the Tast client while any of the services are
        alive.
    """
    if self._tast_client is None:
      self._log.debug('Skipping stop Tast client as it is None.')
      return

    if live_services := self.list_live_services():
      raise Error(
          self._device, 'Cannot stop Tast client because there are other '
          f'alive services: {live_services}')

    self._keyboard_service_wrapper = None
    self._automation_service_wrapper = None

    self._log.debug('Stopping Tast client.')
    if self._tast_client.is_alive:
      with expects.expect_no_raises(
          f'Failed to stop the tast client "{self._tast_client}".'):
        self._tast_client.stop()

  def pause_all(self) -> None:
    raise NotImplementedError()

  def resume_all(self) -> None:
    raise NotImplementedError()

  def resume_services(self, service_aliases: list[str]) -> None:
    raise NotImplementedError()

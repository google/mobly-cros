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

"""A client to manage and communicate with the Tast server on a test machine."""

import os
import time
from typing import Any, Optional, Union

import grpc
from mobly import logger as mobly_logger
from mobly.snippet import client_base
from mobly.snippet import errors

from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import ssh as ssh_lib
from tast.cros.services.cros.audio import cras_control_service_pb2_grpc
from tast.cros.services.cros.bluetooth import bluetooth_ui_service_pb2_grpc
from tast.cros.services.cros.inputs import keyboard_service_pb2_grpc
from tast.cros.services.cros.inputs import touch_service_pb2_grpc
from tast.cros.services.cros.policy import policy_pb2_grpc
from tast.cros.services.cros.ui import automation_service_pb2_grpc
from tast.cros.services.cros.ui import chrome_service_pb2_grpc
from tast.cros.services.cros.ui import conn_service_pb2_grpc
from tast.cros.services.cros.ui import notification_service_pb2_grpc
from tast.cros.services.cros.ui import screen_recorder_service_pb2_grpc
from tast.cros.services.cros.wifi import shill_service_pb2_grpc

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any

# The names of Tast gRPC services that can be used through Mobly Tast client.
# These service names must be exactly the same as the names in the Tast
# gRPC service definition.
TAST_KEYBOARD_SERVICE_NAME = 'KeyboardService'
TAST_SCREEN_RECORDER_SERVICE_NAME = 'ScreenRecorderService'
TAST_CHROME_SERVICE_NAME = 'ChromeService'
TAST_AUTOMATION_SERVICE_NAME = 'AutomationService'
TAST_CONN_SERVICE_NAME = 'ConnService'
TAST_TOUCH_SERVICE_NAME = 'TouchService'
TAST_BLUETOOTH_UI_SERVICE_NAME = 'BluetoothUIService'
TAST_NOTIFICATION_SERVICE_NAME = 'NotificationService'
TAST_SHILL_SERVICE_NAME = 'ShillService'
TAST_CRAS_CONTROL_SERVICE_NAME = 'CrasControlService'
TAST_POLICY_SERVICE_NAME = 'PolicyService'

# The stub classes of Tast gRPC services
_TAST_SERVICES_NAME_TO_STUB_CLASS = {
    TAST_KEYBOARD_SERVICE_NAME: keyboard_service_pb2_grpc.KeyboardServiceStub,
    TAST_SCREEN_RECORDER_SERVICE_NAME: (
        screen_recorder_service_pb2_grpc.ScreenRecorderServiceStub
    ),
    TAST_CHROME_SERVICE_NAME: chrome_service_pb2_grpc.ChromeServiceStub,
    TAST_AUTOMATION_SERVICE_NAME: (
        automation_service_pb2_grpc.AutomationServiceStub
    ),
    TAST_CONN_SERVICE_NAME: conn_service_pb2_grpc.ConnServiceStub,
    TAST_TOUCH_SERVICE_NAME: touch_service_pb2_grpc.TouchServiceStub,
    TAST_BLUETOOTH_UI_SERVICE_NAME: (
        bluetooth_ui_service_pb2_grpc.BluetoothUIServiceStub
    ),
    TAST_NOTIFICATION_SERVICE_NAME: (
        notification_service_pb2_grpc.NotificationServiceStub
    ),
    TAST_SHILL_SERVICE_NAME: shill_service_pb2_grpc.ShillServiceStub,
    TAST_CRAS_CONTROL_SERVICE_NAME: (
        cras_control_service_pb2_grpc.CrasControlServiceStub
    ),
    TAST_POLICY_SERVICE_NAME: policy_pb2_grpc.PolicyServiceStub,
}

# Type aliases for pytype
_GrpcStubType = Union[
    keyboard_service_pb2_grpc.KeyboardServiceStub,
    screen_recorder_service_pb2_grpc.ScreenRecorderServiceStub,
    chrome_service_pb2_grpc.ChromeServiceStub,
    automation_service_pb2_grpc.AutomationServiceStub,
    conn_service_pb2_grpc.ConnServiceStub,
    touch_service_pb2_grpc.TouchServiceStub,
    bluetooth_ui_service_pb2_grpc.BluetoothUIServiceStub,
    notification_service_pb2_grpc.NotificationServiceStub,
    shill_service_pb2_grpc.ShillServiceStub,
    cras_control_service_pb2_grpc.CrasControlServiceStub,
    policy_pb2_grpc.PolicyServiceStub,
]

# The python code to find an unused port. We do not use portpicker here
# because the native python on CrOS doesn't contain the library portpicker.
PY_CODE_TO_FIND_UNUSED_PORT = """
import socket
s=socket.socket()
s.bind(("", 0))
print(s.getsockname()[1])
s.close()
"""


class TastClient(client_base.ClientBase):
  """A client to manage and communicate with the Tast server on a test machine.

  The Tast client manages the lifecycle of the Tast server, and sends gRPC
  requests to call services on the Tast server.

  This class utilizes the Mobly ClientBase class's lifecycle management logic
  and overrides the logic regarding sending RPCs.

  The errors related to this class uses the prefix
  "<TastClient|{device_controller.debug_tag}>"

  Attributes:
    log: The logger adapter for the CrOS device.
    is_alive: True if the Tast session service is alive; False otherwise.
  """

  def __init__(self, device: 'CrosDevice') -> None:
    """Initializes the Tast client instance.

    Args:
      device: The controller object for the CrOS device with which the Tast
        client is communicating.
    """
    super().__init__(package='TastClient', device=device)
    self._device = device
    self.log = mobly_logger.PrefixLoggerAdapter(
        device.log,
        {mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX: '[TastClient]'},
    )
    self._device_port = None
    self._host_port = 0
    self._is_device_port_forwarded = False
    self._channel = None
    self._tast_service_stubs = {}
    self._tast_server_process: Optional[ssh_lib.RemotePopen] = None

  def __repr__(self) -> str:
    return f'<TastClient|{self._device.debug_tag}>'

  @property
  def is_alive(self) -> bool:
    """True if the Tast session service is alive; False otherwise."""
    return (self._tast_server_process is not None and
            self._tast_server_process.poll() is None)

  def before_starting_server(self) -> None:
    """Performs the preparation steps before starting the remote server.

    This method performs following preparation steps:
    1. Clear any Tast server process running on the remote device.
    2. Ensure the port that the Tast server is going to listen to is free on the
      device.
    """
    self._clear_any_server_process_on_device()
    self._get_avaible_device_port()
    self._ensure_device_port_free()

  def _get_avaible_device_port(self) -> None:
    """Gets an available device port and sets it to self._device_port."""
    if self._device_port is not None:
      self.log.debug('Device port is already set to %d', self._device_port)
      return

    # We use a script to find an unused port because the server output does not
    # contain the server listening port
    cmd_to_find_unused_port = f"python -c '{PY_CODE_TO_FIND_UNUSED_PORT}'"
    new_device_port = self._device.ssh.execute_command(
        cmd_to_find_unused_port, ignore_error=False)
    self.log.debug('Setting device port to %s', new_device_port)
    self._device_port = int(new_device_port)

  def _ensure_device_port_free(self) -> None:
    """Ensures the device port is free on the remote device."""
    output = self._device.ssh.execute_command(
        f'lsof -i :{self._device_port}', ignore_error=True)
    if output:
      raise errors.ServerStartPreCheckError(
          self._device,
          f'Cannot start Tast server because the port {self._device_port} '
          f'is occupied by the process:\n{output}')

  def _clear_any_server_process_on_device(self) -> None:
    """Clears any Tast server process running on the remote device."""
    tast_server_command_name = os.path.basename(constants.TAST_SERVER_EXE_PATH)
    self._device.ssh.execute_command(
        f'killall -9 {tast_server_command_name}', ignore_error=True)

  def check_server_proc_running(self) -> None:
    """Checks whether Tast server process on host is running.

    This function only checks the status of the server process on host so it is
    quick and won't affect performance.

    If the server process object is None or it has already died, this will raise
    an error.

    Raises:
      ValueError: if server process is None.
      errors.ServerDiedError: if server process has already died.
    """
    if self._tast_server_process is None:
      raise ValueError('Trying to check server process status when '
                       'self._tast_server_process is None.')

    exit_code = self._tast_server_process.poll()
    if exit_code is None:
      return

    self._tast_server_process = None
    raise errors.ServerDiedError(
        self, 'The Tast server process has exited in advance unexpectedly. Got '
        f'exit code: {exit_code}.')

  def start_server(self) -> None:
    """Starts the Tast server on the test machine."""
    cmd_str = self._construct_server_startup_cmd()
    self.log.debug('Running the server startup command: %s', cmd_str)
    tast_server_log_path = os.path.join(self._device.log_path,
                                        'tast_server.log')
    self._tast_server_process = self._device.ssh.start_remote_process(
        cmd_str, get_pty=True, output_file_path=tast_server_log_path)

  def _construct_server_startup_cmd(self) -> str:
    return ' '.join([
        constants.TAST_SERVER_EXE_PATH,
        '-rpctcp',  # The mode -rpctcp is for external users to use Tast Server
        f'-port {self._device_port}',
    ])

  def make_connection(self) -> None:
    """Makes the connection to the Tast server on the test machine.

    This function includes following steps:
    1. Forward the server listening port on the test machine to host.
    2. Create the gRPC channel to the server using the forwarded port.
    """
    self._forward_device_port()
    self._build_grpc_channel()

  def _forward_device_port(self) -> None:
    self.log.debug('Forwarding device port %d to host.', self._device_port)
    self._host_port = self._device.ssh.forward_port(self._device_port,
                                                    self._host_port)
    self._is_device_port_forwarded = True
    self.log.debug('Forwarded device port %d to host port %d.',
                   self._device_port, self._host_port)

  def _build_grpc_channel(self) -> None:
    """Builds the gRPC channel with the Tast server.

    This function waits until the channel is ready.
    """
    self.check_server_proc_running()
    server_target = f'localhost:{self._host_port}'
    self.log.debug('Creating an insecure gRPC channel to server target: %s',
                   server_target)
    self._channel = grpc.insecure_channel(server_target)
    grpc.channel_ready_future(self._channel).result(
        timeout=constants.TAST_SERVER_CONNECTION_TIMEOUT_SEC)

  def stop(self) -> None:
    """Releases all the resources acquired in `start_server`."""
    self.log.debug('Stopping Tast client.')
    self.close_connection()
    self._kill_tast_server()
    self.log.debug('Tast client stopped.')

  def close_connection(self):
    """Releases all the resources acquired in `make_connection`.

    This function closes the gRPC channel and stops the port forwarding process.
    """
    try:
      # TODO: Remove the temporary workaround to sleep 3 seconds
      # after we figure out the solution for the flake in channel close, which
      # sometimes causes the test to fail.
      time.sleep(3)
      self._close_grpc_channel()
    finally:
      # Make sure not to cause resource leak on host machine even when failed to
      # stop Tast client and server
      self._stop_port_forwarding()

  def _close_grpc_channel(self) -> None:
    # The stubs hold the references to the channel object, so destroy them first
    self._tast_service_stubs.clear()

    if self._channel is not None:
      self._channel.close()
      self._channel = None
      self.log.debug('gRPC channel closed.')

  def _stop_port_forwarding(self) -> None:
    if self._is_device_port_forwarded:
      self._device.ssh.stop_port_forwarding(self._host_port)
      self._host_port = 0
      self._is_device_port_forwarded = False
      self.log.debug('Stopped forwarding device address %s:%d to host.',
                     self._device.hostname, self._device_port)

  def _kill_tast_server(self) -> None:
    """Kills the Tast server.

    This function will check that the server process didn't exit in advance
    unexpectedly, otherwise throws an error.
    """
    if self._tast_server_process is None:
      return

    # Check that server didn't exit in advance unexpectedly
    self.check_server_proc_running()
    self._tast_server_process: ssh_lib.RemotePopen
    try:
      self._tast_server_process.send_signal(
          signal_id=15, timeout=constants.TAST_SERVER_TERMINATE_TIMEOUT_SEC)
    except ssh_lib.RemoteTimeoutError as e:
      self.log.debug(
          'Tast server Termination timed out: %s. Force killing the Tast '
          'server.', e)
      self._tast_server_process.kill()
    self._tast_server_process = None
    self._device_port = None
    self.log.debug('Tast server process was killed.')

  def get_or_create_grpc_stub(self, service_name: str) -> _GrpcStubType:
    """Gets or creates the gRPC service stub with the given service name.

    For a given service, this function creates the stub object for the first
    time it is requested, and caches it for subsequent requests. The stubs are
    thread-safe. This caching avoids the time overhead of repeatedly creating
    stubs.

    Args:
      service_name: The service name.

    Returns:
      The gRPC service stub object.

    Raises:
      ValueError: If the service with the given name doesn't exist.
    """
    with self._lock:
      if stub := self._tast_service_stubs.get(service_name):
        return stub

      stub_class = _TAST_SERVICES_NAME_TO_STUB_CLASS.get(service_name)
      if stub_class is None:
        raise ValueError(f'Got unknown service name: {service_name}')

      stub = stub_class(self._channel)
      self._tast_service_stubs[service_name] = stub
      return stub

  # TODO: Temporarily override these abstract methods during the
  # Tast client implementation. This is required as we need to initialize the
  # instances in unit tests.

  def restore_server_connection(self, port: Optional[int] = None):
    raise NotImplementedError('To be implemented.')

  def send_rpc_request(self, request: str):
    raise NotImplementedError('To be implemented.')

  def handle_callback(self, callback_id: str, ret_value: Any,
                      rpc_func_name: str):
    raise NotImplementedError('To be implemented.')

  def __del__(self):
    # Override the destructor to not call close_connection for now.
    pass

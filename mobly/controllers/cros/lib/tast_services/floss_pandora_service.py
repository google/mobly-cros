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

"""Manages the Floss pandora server life cycle."""

from typing import Any

from mobly import logger as mobly_logger
from mobly import utils
from mobly.controllers.android_device_lib.services import base_service
import portpicker

PANDORA_SERVER_GRPC_PORT = 8999
CROS_PANDORA_SERVER_PACKAGE = 'floss.pandora.server.server'

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any


class FlossPandoraService(base_service.BaseService):
  """Manages the Pandora gRPC server on a CrosDevice."""
  _port = None
  _remote_server_process = None
  _forward_grpc_port_process = None

  def __init__(
      self, device: 'CrosDevice', configs: Any | None = None):
    super().__init__(device, configs)

    self._log = mobly_logger.PrefixLoggerAdapter(self._device.log, {
        mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX:
            '[FlossPandoraService]'
    })
    self._device = device
    self._is_alive = False

  @property
  def is_alive(self) -> bool:
    """True if the Floss Pandora server service is alive; False otherwise."""
    return self._is_alive

  @property
  def port(self) -> int | None:
    """Returns the port of the pandora service."""
    return self._port if self._forward_grpc_port_process is not None else None

  def start(self) -> None:
    """Sets up and starts the Floss Pandora server on the Cros device."""
    if self.is_alive:
      return

    if self._remote_server_process is not None:
      raise RuntimeError(
          'Remote server process exists when calling stop.')

    if self._forward_grpc_port_process is not None:
      raise RuntimeError(
          'Port forwarding process exists when calling stop.')

    self._log.info('Starting Floss pandora service.')

    self._port = portpicker.pick_unused_port()

    # The Python SSH package `paramiko` has socket issues with
    # gRPC channel so we use ssh for port forwarding.
    # Closing the stdin in the utils.start_standing_subprocess()
    # causes the SSH port forwarding to fail. Adding the -tt option
    # fixes this issue.
    cmd = [
        'ssh',
        '-tt',
        '-L',
        f'{self._port}:localhost:{PANDORA_SERVER_GRPC_PORT}',
        self._device.hostname
    ]

    self._log.debug('Forwarding port %s to the remote host.', self._port)

    self._forward_grpc_port_process = utils.start_standing_subprocess(
        cmd)

    self._remote_server_process = self._device.ssh.start_remote_process(
        ' '.join(['python', '-m', CROS_PANDORA_SERVER_PACKAGE]),
    )

    self._is_alive = True

  def stop(self) -> None:
    """Stops and cleans up the Pandora server on the Cros device."""
    if not self.is_alive:
      return

    if self._remote_server_process is None:
      self._log.warning(
          'Remote server process is not alive when calling stop.')
    else:
      self._log.info('Stopping Floss pandora service.')
      self._remote_server_process.kill()
      self._remote_server_process = None

    if self._forward_grpc_port_process is None:
      self._log.warning(
          'Port forwarding process is not alive when calling stop.')
    else:
      self._log.info('Stopping Floss pandora service.')
      utils.stop_standing_subprocess(self._forward_grpc_port_process)
      self._forward_grpc_port_process = None

    self._is_alive = False

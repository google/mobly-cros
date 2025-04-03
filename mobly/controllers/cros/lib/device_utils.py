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

"""Utils for operating CrOS devices."""

import enum
import pathlib
import typing
from typing import Any, Optional
import uuid

from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import tast_client
from tast.cros.services.cros.inputs import touch_service_pb2
from tast.cros.services.cros.inputs import touch_service_pb2_grpc

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any

# The timeout to wait for the root filesystem verification removal.
_REMOVE_ROOTFS_VERIFICATION_COMMAND_TIMEOUT_SEC = 60

# CrOS shell commands to operate Wi-Fi
_GET_CROS_WLAN = 'iw dev | awk \'$1=="Interface"{print $2}\''
_GET_CROS_SSID = 'iw dev {wlan_name} link | awk \'$1=="SSID:"{{print $2}}\''
_CONNECT_TO_WIFI = (
    '/usr/local/autotest/cros/scripts/wifi connect {wifi_ssid} {wifi_psk}')


def is_rootfs_writable(crosd: 'CrosDevice') -> bool:
  """Checks CrOS root filesystem is writable or not.

  Args:
    crosd: The CrOS device controller object.

  Returns:
    True if the CrOS root filesystem is writable; False otherwise.
  """
  random_dir_path = pathlib.PurePosixPath(constants.CHROME_LOCATION,
                                          str(uuid.uuid4()))
  try:
    crosd.ssh.make_dirs(str(random_dir_path))
    crosd.ssh.rm_dir(str(random_dir_path))
    return True
  except IOError:
    return False


def remove_rootfs_verification_if_not(crosd: 'CrosDevice') -> None:
  """Removes CrOS root filesystem verification.

  Args:
    crosd: The CrOS device controller object.

  Raises:
    RuntimeError: If failed to remove root filesystem verification.
  """
  if is_rootfs_writable(crosd):
    crosd.log.info('Root filesystem is already writable, skip removing.')
    return

  crosd.log.info('Removing root filesystem verification ...')
  crosd.ssh.execute_command(
      '/usr/share/vboot/bin/make_dev_ssd.sh '
      '--remove_rootfs_verification --force',
      timeout=_REMOVE_ROOTFS_VERIFICATION_COMMAND_TIMEOUT_SEC)
  crosd.reboot()
  if not is_rootfs_writable(crosd):
    raise RuntimeError('Failed to remove root filesystem verification. '
                       'Although the command executed successfully, the '
                       'filesystem is still not writable.')
  crosd.log.debug('Root filesystem verification removed.')


def connect_to_wifi(crosd: 'CrosDevice',
                    wifi_ssid: str,
                    wifi_psk: str = '') -> None:
  """Connects the CrOS device to specific Wi-Fi.

  Args:
    crosd: The CrOS device controller object.
    wifi_ssid: The Wi-Fi SSID.
    wifi_psk: The password of the Wi-Fi SSID.

  Raises:
    ValueError: If the received WiFi SSID is empty.
  """
  if not wifi_ssid:
    raise ValueError('Wi-Fi SSID cannot be empty.')

  if get_connected_wifi_ssid(crosd) == wifi_ssid:
    crosd.log.info('Already connected to Wi-Fi %s', wifi_ssid)
    return

  cmd = _CONNECT_TO_WIFI.format(wifi_ssid=wifi_ssid, wifi_psk=wifi_psk)
  crosd.ssh.execute_command(cmd)
  crosd.log.info('Connected to Wi-Fi %s', wifi_ssid)


def get_connected_wifi_ssid(crosd: 'CrosDevice') -> Optional[str]:
  """Gets the connected Wi-Fi SSID on the CrOS device, None if not connected.

  Args:
    crosd: The CrOS device controller object.

  Returns:
    The Wi-Fi SSID.
  """
  wlan_name = crosd.ssh.execute_command(_GET_CROS_WLAN)
  wlan_name = crosd.ssh.execute_command(
      _GET_CROS_SSID.format(wlan_name=wlan_name))
  if not wlan_name:
    wlan_name = None
  return wlan_name


class _SwipeType(enum.Enum):
  """The enumeration of supported swipe types."""

  # One finger swipe
  ONE_FINGER_SWIPE = 1

  # Two finger swipe
  TWO_FINTER_SWIPE = 2

  # Three finger swipe
  THREE_FINTER_SWIPE = 3


def swipe(crosd: 'CrosDevice', sx: int, sy: int, ex: int, ey: int,
          steps: int = 100):
  """Performs a swipe from one coordinate to another.

  Args:
    crosd: The CrOS device controller object.
    sx: The X coordinate of the starting point.
    sy: The Y coordinate of the starting point.
    ex: The X coordinate of the end point.
    ey: The Y coordinate of the end point.
    steps: The number of steps for the swipe action. Each step execution is
      throttled to 5 milliseconds, so for 100 steps, the swipe will take
      around 0.5 seconds to complete.

  Raises:
    tast_service_manager.MissingTastSessionError: If trying to perform a swipe
      when the TastSessionService is not alive.
  """
  if not crosd.services.is_tast_session_service_alive():
    # pytype: disable=import-error
    from mobly.controllers.cros.lib import tast_service_manager  # pylint: disable=g-import-not-at-top
    # pytype: enable=import-error
    raise tast_service_manager.MissingTastSessionError(
        crosd, 'Performing a swipe when the TastSessionService is not alive is '
        'not supported.')

  stub = crosd.tast_client.get_or_create_grpc_stub(
      tast_client.TAST_TOUCH_SERVICE_NAME)
  stub = typing.cast(touch_service_pb2_grpc.TouchServiceStub, stub)

  # The underlying implementation requires to declare how long the swipe should
  # last. To be consistent with the swipe method in Android UiAutomator, this
  # interface exposes the `steps` argument and each step is about 5ms.
  time_ms = 5 * steps

  touches = _SwipeType.ONE_FINGER_SWIPE.value
  request = touch_service_pb2.SwipeRequest(
      x0=sx,
      y0=sy,
      x1=ex,
      y1=ey,
      touches=touches,
      time_milli_seconds=time_ms,
  )

  crosd.log.debug('Performing a swipe operation with gRPC request: %s', request)
  stub.Swipe(request)

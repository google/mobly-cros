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

"""Utils for controlling bluetooth on CrOS devices through UI interactions.

NOTE: All the functions in this module depends on the TastSessionService. So
make sure it is running when you are calling functions from this module.
"""

from collections.abc import Sequence
import typing
from typing import Any

from google.protobuf import empty_pb2
from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import tast_client
from mobly.controllers.cros.lib import tast_service_manager
from tast.cros.services.cros.bluetooth import bluetooth_ui_service_pb2
from tast.cros.services.cros.bluetooth import bluetooth_ui_service_pb2_grpc

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any


# Aliases for fast pair protocol
FAST_PAIR_PROTOCOL_NULL = (
    bluetooth_ui_service_pb2.FastPairProtocol.FAST_PAIR_PROTOCOL_NULL
)
FAST_PAIR_PROTOCOL_SUBSEQUENT = (
    bluetooth_ui_service_pb2.FastPairProtocol.FAST_PAIR_PROTOCOL_SUBSEQUENT
)
FAST_PAIR_PROTOCOL_INITIAL = (
    bluetooth_ui_service_pb2.FastPairProtocol.FAST_PAIR_PROTOCOL_INITIAL
)
FAST_PAIR_PROTOCOL_RETROACTIVE = (
    bluetooth_ui_service_pb2.FastPairProtocol.FAST_PAIR_PROTOCOL_RETROACTIVE
)

_DEFAULT_TIMEOUT = constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC


def _get_grpc_service_stub(
    device: 'CrosDevice',
) -> bluetooth_ui_service_pb2_grpc.BluetoothUIServiceStub:
  stub = device.tast_client.get_or_create_grpc_stub(
      tast_client.TAST_BLUETOOTH_UI_SERVICE_NAME
  )
  return typing.cast(bluetooth_ui_service_pb2_grpc.BluetoothUIServiceStub, stub)


@tast_service_manager.assert_tast_session_service_alive
def pair_device_with_quick_settings(
    device: 'CrosDevice', advertise_name: str
) -> None:
  """Pairs with the device through UI interactions with Quick Settings.

  This function will check that the popup "{advertise_name} connected" appears
  as the success condition. RPC will fail if failed to pair the specified
  device, or the device is paired but is not connected.

  Args:
    device: The controller object for the CrOS device.
    advertise_name: The advertise name of the bluetooth device to be paired
      with.
  """
  request = bluetooth_ui_service_pb2.PairDeviceWithQuickSettingsRequest(
      advertisedName=advertise_name,
  )
  stub = _get_grpc_service_stub(device)
  stub.PairDeviceWithQuickSettings(request, timeout=_DEFAULT_TIMEOUT)


@tast_service_manager.assert_tast_session_service_alive
def forget_connected_bluetooth_device(
    device: 'CrosDevice', device_name: str
) -> None:
  """Forgets the devices are saved on the Device Detail subpage.

  Args:
    device: The controller object for the CrOS device.
    device_name: The device name.
  """
  request = bluetooth_ui_service_pb2.ForgetBluetoothDeviceRequest(
      device_name=device_name,
  )
  stub = _get_grpc_service_stub(device)
  stub.ForgetBluetoothDevice(request, timeout=_DEFAULT_TIMEOUT)


@tast_service_manager.assert_tast_session_service_alive
def pair_with_fast_pair_notification(
    device: 'CrosDevice',
    protocol: bluetooth_ui_service_pb2.FastPairProtocol,
) -> None:
  """Pairs a device through UI interactions with the fast pair notification.

  This assumes that there is already a fast pair notification on the CrOS
  device.

  Args:
    device: The controller object for the CrOS device.
    protocol: The fast pair protocol.
  """
  request = bluetooth_ui_service_pb2.PairWithFastPairNotificationRequest(
      protocol=protocol,
  )
  stub = _get_grpc_service_stub(device)
  stub.PairWithFastPairNotification(request, timeout=_DEFAULT_TIMEOUT)


@tast_service_manager.assert_tast_session_service_alive
def remove_all_saved_devices(device: 'CrosDevice') -> None:
  """Removes all saved devices from the Saved Devices subpage.

  NOTE: Note that devices that only appear on the "Previously connected" subpage
  and not on the "Devices saved to your account" subpage will not be removed.

  Args:
    device: The controller object for the CrOS device.
  """
  request = empty_pb2.Empty()
  stub = _get_grpc_service_stub(device)
  stub.RemoveAllSavedDevices(
      request,
      timeout=_DEFAULT_TIMEOUT,
  )


@tast_service_manager.assert_tast_session_service_alive
def confirm_saved_devices_state(
    device: 'CrosDevice', device_names: Sequence[str]
) -> None:
  """Confirms the devices are saved on the Saved Devices subpage.

  NOTE: The order of the device name list DOES matter.

  This confirms that the given device names are exactly the same as the
  devices in the "Devices saved to your account" subpage. RPC will fail if
  failed the saved devices doesn't match the one provided.

  Args:
    device: The controller object for the CrOS device.
    device_names: The device name list.
  """
  request = bluetooth_ui_service_pb2.ConfirmSavedDevicesStateRequest(
      device_names=device_names,
  )
  stub = _get_grpc_service_stub(device)
  stub.ConfirmSavedDevicesState(request, timeout=_DEFAULT_TIMEOUT)


@tast_service_manager.assert_tast_session_service_alive
def close_notifications(device: 'CrosDevice') -> None:
  """Closes all notifications."""
  request = empty_pb2.Empty()
  stub = _get_grpc_service_stub(device)
  stub.CloseNotifications(request, timeout=_DEFAULT_TIMEOUT)

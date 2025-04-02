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

"""Utils for controlling CRAS control interface on CrOS devices.

NOTE: All the functions in this module depends on the TastSessionService. So
make sure it is running when you are calling functions from this module.
"""

import typing

from google.protobuf import empty_pb2
from mobly.controllers.cros import cros_device
from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import tast_client
from tast.cros.services.cros.audio import cras_control_service_pb2
from tast.cros.services.cros.audio import cras_control_service_pb2_grpc
from tast.cros.services.cros.audio import cras_types_pb2


_DEFAULT_TIMEOUT = constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC


def _cras_stub(
    device: cros_device.CrosDevice,
) -> cras_control_service_pb2_grpc.CrasControlServiceStub:
  stub = device.tast_client.get_or_create_grpc_stub(
      tast_client.TAST_CRAS_CONTROL_SERVICE_NAME
  )
  return typing.cast(cras_control_service_pb2_grpc.CrasControlServiceStub, stub)


def restart_cras(device: cros_device.CrosDevice) -> None:
  """Restarts the cras job and waits for it to be back up before returning.

  Args:
    device: The controller object for the CrOS device.
  """
  _cras_stub(device).RestartCras(
      empty_pb2.Empty(), timeout=_DEFAULT_TIMEOUT
  )


def set_force_hfp_swb_enabled(
    device: cros_device.CrosDevice, force_hfp_swb_enabled: bool
) -> None:
  """Sets the state to enable or disable bluetooth HFP SWB.

  Args:
    device: The controller object for the CrOS device.
    force_hfp_swb_enabled: True to enable force HFP SWB, False to disable.
  """
  request = cras_control_service_pb2.SetForceHfpSwbEnabledRequest(
      force_hfp_swb_enabled=force_hfp_swb_enabled,
  )
  _cras_stub(device).SetForceHfpSwbEnabled(request, timeout=_DEFAULT_TIMEOUT)


def get_force_hfp_swb_enabled(
    device: cros_device.CrosDevice,
) -> bool:
  """Gets the force_hfp_swb_enabled state.

  Args:
    device: The controller object for the CrOS device.

  Returns:
    True if HFP SWB is enabled, False otherwise.
  """
  return _cras_stub(device).GetForceHfpSwbEnabled(
      empty_pb2.Empty(), timeout=_DEFAULT_TIMEOUT
  ).force_hfp_swb_enabled


def get_nodes(
    device: cros_device.CrosDevice,
) -> list[cras_types_pb2.CrasNode]:
  """Returns CRAS audio nodes.

  Args:
    device: The controller object for the CrOS device.

  Returns:
    List of CRAS nodes.
  """
  return (
      _cras_stub(device)
      .GetNodes(empty_pb2.Empty(), timeout=_DEFAULT_TIMEOUT)
      .nodes
  )


def selected_input_node(
    device: cros_device.CrosDevice,
) -> cras_types_pb2.CrasNode:
  """Calls GetNodes and returns the active input node.

  Args:
    device: The controller object for the CrOS device.

  Returns:
    The active input node.
  """
  return (
      _cras_stub(device)
      .SelectedInputNode(empty_pb2.Empty(), timeout=_DEFAULT_TIMEOUT)
      .selected_input_node
  )


def selected_output_node(
    device: cros_device.CrosDevice,
) -> cras_types_pb2.CrasNode:
  """Calls SelectedOutputNode and returns the active output node.

  Args:
    device: The controller object for the CrOS device.

  Returns:
    The active output node.
  """
  return (
      _cras_stub(device)
      .SelectedOutputNode(empty_pb2.Empty(), timeout=_DEFAULT_TIMEOUT)
      .selected_output_node
  )


def set_active_input_node(
    device: cros_device.CrosDevice,
    node_id: int,
) -> None:
  """Calls SetActiveInputNode with the given node ID.

  Args:
    device: The controller object for the CrOS device.
    node_id: The node id of the input node to be set as active.
  """
  request = cras_control_service_pb2.SetActiveInputNodeRequest(node_id=node_id)
  _cras_stub(device).SetActiveInputNode(request, timeout=_DEFAULT_TIMEOUT)


def set_active_output_node(
    device: cros_device.CrosDevice,
    node_id: int,
) -> None:
  """Calls SetActiveOutputNode with the given node ID.

  Args:
    device: The controller object for the CrOS device.
    node_id: The node id of the output node to be set as active.
  """
  request = cras_control_service_pb2.SetActiveOutputNodeRequest(node_id=node_id)
  _cras_stub(device).SetActiveOutputNode(request, timeout=_DEFAULT_TIMEOUT)

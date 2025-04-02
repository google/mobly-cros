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

"""The wrapper classes for users to easily call Tast services."""

import logging
import typing

import grpc
from mobly import logger as mobly_logger

from google.protobuf import descriptor
from google.protobuf import message
from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import tast_client
from tast.cros.services.cros.inputs import keyboard_service_pb2
from tast.cros.services.cros.inputs import keyboard_service_pb2_grpc
from tast.cros.services.cros.ui import automation_service_pb2
from tast.cros.services.cros.ui import automation_service_pb2_grpc


class InvalidGrpcMethodCallError(Exception):
  """Raised when trying to invoke a gRPC call with invalid arguments."""


def _assert_request_and_grpc_method_match(
    request: message.Message,
    *,
    service_descriptor: descriptor.ServiceDescriptor,
    method_name: str,
):
  """Asserts that the request type and gRPC method match.

  Args:
    request: The request message to check.
    service_descriptor: The descriptor of the gRPC service to use.
    method_name: The name of the method to call with the given request message.

  Raises:
    InvalidGrpcMethodCallError: If got an invalid method name or the request
      type and gRPC method didn't match.
  """
  method_descriptor = service_descriptor.methods_by_name.get(method_name)
  if method_descriptor is None:
    raise InvalidGrpcMethodCallError(
        f'Got unknown method name "{method_name}" for service '
        f'"{service_descriptor.full_name}"')

  method_request_type_name = method_descriptor.input_type.full_name

  request_type_name = type(request).DESCRIPTOR.full_name

  if method_request_type_name != request_type_name:
    raise InvalidGrpcMethodCallError(
        f'Expect request type "{method_request_type_name}" in gRPC method '
        f'"{method_descriptor.full_name}", got "{request_type_name}".')


def _invoke_grpc_call(
    grpc_func: grpc.UnaryUnaryMultiCallable,
    grpc_func_name: str,
    request: message.Message,
    logger: logging.LoggerAdapter,
    timeout_sec: int = constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC,
) -> message.Message:
  """Invokes a gRPC call with the given request and returns the response.

  Args:
    grpc_func: The callable object of the rpc method to invoke.
    grpc_func_name: The name of the rpc method to invoke.
    request: The request object for invoking the rpc method.
    logger: The logger used for printing information before and after invoking
      the rpc method.
    timeout_sec: The timeout seconds to wait for the RPC call to finish.

  Returns:
    The gRPC method response.
  """
  logger.debug(
      'Invoking a gRPC call. RPC method: %s, timeout: %d, request: %s',
      grpc_func_name,
      timeout_sec,
      request,
  )
  response = grpc_func(request, timeout=timeout_sec)
  logger.debug('gRPC call done. Response: %s', response)
  return response


class KeyboardServiceWrapper:
  """The wrapper class for invoking rpc methods in Tast Keyboard Service.

  Attributes:
    log: A logger adapted from a given logger, which adds the identifier
      '[KeyboardServiceWrapper]' to each log line: '<prefix of the given logger>
      [KeyboardServiceWrapper] <message>'.
  """

  def __init__(self, tast_client_object: tast_client.TastClient,
               logger: logging.LoggerAdapter) -> None:
    """Initializes the KeyboardServiceWrapper instance.

    Args:
      tast_client_object: The Tast client for getting gRPC service stub and
        sending gRPC requests.
      logger: A given logger which should contain basic debug information in
        each log line, e.g. the device identifier. Typically the logger of the
        CrOS device controller is used.
    """
    self.log = mobly_logger.PrefixLoggerAdapter(
        logger,
        {
            mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX:
                '[KeyboardServiceWrapper]'
        },
    )
    self._tast_client = tast_client_object

  def _get_grpc_service_stub(
      self) -> keyboard_service_pb2_grpc.KeyboardServiceStub:
    stub = self._tast_client.get_or_create_grpc_stub(
        tast_client.TAST_KEYBOARD_SERVICE_NAME)
    return typing.cast(keyboard_service_pb2_grpc.KeyboardServiceStub, stub)

  def type(self, key: str) -> message.Message:
    """Types the given string on the test device.

    This function supports characters that can be typed using a QWERTY keyboard,
    including the ones that require pressing Shift key, e.g. uppercase letters.
    More details about the supported characters and requirements per:
    http://chromium.googlesource.com/chromiumos/platform/tast-tests/+/refs/heads/main/src/go.chromium.org/tast-tests/cros/services/cros/inputs/keyboard_service.proto

    Args:
      key: The string to be typed on the test device.

    Returns:
      The gRPC method response.
    """
    return _invoke_grpc_call(
        grpc_func=self._get_grpc_service_stub().Type,
        grpc_func_name='Type',
        request=keyboard_service_pb2.TypeRequest(key=key),
        logger=self.log)

  def accel(self, key: str) -> message.Message:
    """Simulates the given accelerator on the test device.

    Accelerators (a.k.a. hotkey) are described as a sequence of '+'-separated,
    case-insensitive key characters or names, e.g. "Ctrl+t", "Ctrl+Shift+/".
    More details about the supported characters per:
    http://chromium.googlesource.com/chromiumos/platform/tast-tests/+/refs/heads/main/src/go.chromium.org/tast-tests/cros/services/cros/inputs/keyboard_service.proto

    Args:
      key: The string describing the accelerator to be simulated.

    Returns:
      The gRPC method response.
    """
    return _invoke_grpc_call(
        grpc_func=self._get_grpc_service_stub().Accel,
        grpc_func_name='Accel',
        request=keyboard_service_pb2.AccelRequest(key=key),
        logger=self.log)

  def accel_press(self, key: str) -> message.Message:
    """Simulates pressing the given accelerator on the test device.

    Args:
      key: The string describing the accelerator to be pressed.

    Returns:
      The gRPC method response.
    """
    return _invoke_grpc_call(
        grpc_func=self._get_grpc_service_stub().AccelPress,
        grpc_func_name='AccelPress',
        request=keyboard_service_pb2.AccelPressRequest(key=key),
        logger=self.log)

  def accel_release(self, key: str) -> message.Message:
    """Simulates releasing the given accelerator on the test device.

    Args:
      key: The string describing the accelerator to be released.

    Returns:
      The gRPC method response.
    """
    return _invoke_grpc_call(
        grpc_func=self._get_grpc_service_stub().AccelRelease,
        grpc_func_name='AccelRelease',
        request=keyboard_service_pb2.AccelReleaseRequest(key=key),
        logger=self.log)


class AutomationServiceWrapper:
  """The wrapper class for invoking rpc methods in Tast Automation service.

  This class exposes all the RPC methods defined in the Tast Automation service.
  Users can use the method name and request message object to trigger those  RPC
  methods.

  Example usage:

  .. code-block:: python

    request = automation_service_pb2.RightClickRequest(
        finder=automation_service_pb2.Finder(
            node_withs=[
                automation_service_pb2.NodeWith(name='Add shortcut'),
            ]))
    automation_service_wrapper.invoke_grpc_call('RightClick', request)

  Full list of RPC methods and messages per:
  http://chromium.googlesource.com/chromiumos/platform/tast-tests/+/refs/heads/main/src/go.chromium.org/tast-tests/cros/services/cros/ui/automation_service.proto

  Attributes:
    log: A logger adapted from a given logger, which adds the identifier
      '[AutomationServiceWrapper]' to each log line: '<prefix of the given
      logger> [AutomationServiceWrapper] <message>'.
  """

  def __init__(self, tast_client_object: tast_client.TastClient,
               logger: logging.LoggerAdapter) -> None:
    """Initializes the AutomationServiceWrapper instance.

    Args:
      tast_client_object: The Tast client for getting gRPC service stub and
        sending gRPC requests.
      logger: A given logger which should contain basic debug information in
        each log line, e.g. the device identifier. Typically the logger of the
        CrOS device controller is used.
    """
    self.log = mobly_logger.PrefixLoggerAdapter(
        logger,
        {
            mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX:
                '[AutomationServiceWrapper]'
        },
    )
    self._tast_client = tast_client_object

  def _get_grpc_service_stub(
      self) -> automation_service_pb2_grpc.AutomationServiceStub:
    stub = self._tast_client.get_or_create_grpc_stub(
        tast_client.TAST_AUTOMATION_SERVICE_NAME)
    return typing.cast(automation_service_pb2_grpc.AutomationServiceStub, stub)

  def invoke_grpc_call(self, method_name: str,
                       request: message.Message) -> message.Message:
    """Invokes the given gRPC call of the Tast Automation Service.

    Args:
      method_name: The name of the gRPC method to invoke.
      request: The request message for invoking the rpc method.

    Returns:
      The gRPC method response.
    """

    service_descriptor = automation_service_pb2.DESCRIPTOR.services_by_name[
        tast_client.TAST_AUTOMATION_SERVICE_NAME]
    _assert_request_and_grpc_method_match(
        request, service_descriptor=service_descriptor, method_name=method_name)

    stub = self._get_grpc_service_stub()
    grpc_func = getattr(stub, method_name)
    return _invoke_grpc_call(
        grpc_func=grpc_func,
        grpc_func_name=method_name,
        request=request,
        logger=self.log)

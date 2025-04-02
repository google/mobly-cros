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

"""Utils for operating notifications on CrOS devices."""

from collections.abc import Sequence
import typing
from typing import Any, cast

import grpc

from google.protobuf import empty_pb2
from mobly.controllers.cros.lib import tast_client
from mobly.controllers.cros.lib import tast_service_manager
from tast.cros.services.cros.ui import notification_service_pb2
from tast.cros.services.cros.ui import notification_service_pb2_grpc

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any

GRPC_REQUEST_DEFAULT_TIMEOUT = 500

# GRPC error messages thrown in the Tast notification service.
_GRPC_ERROR_MSG_NOTIFICATION_NOT_GONE = (
    'failed to wait for notification to disappear'
)
_GRPC_ERROR_MSG_NOTIFICATION_DID_NOT_APPEAR = 'no wanted notification'

# Error messages thrown in this module.
_ERROR_MSG_NOTIFICATION_DID_NOT_APPEAR = (
    'Failed to wait for an eligible notification with gRPC request: {request}'
)

_WAIT_FOR_NOTIFICATION_DEFAULT_TIMEOUT_SEC = 60


class NotificationServiceError(Exception):
  """Base error type for this module."""

  def __init__(self, device: 'CrosDevice', message: str) -> None:
    super().__init__(f'{repr(device)} {message}')


@tast_service_manager.assert_tast_session_service_alive
def close_all_notifications(crosd: 'CrosDevice') -> None:
  """Closes all the notifications."""
  stub = crosd.tast_client.get_or_create_grpc_stub(
      tast_client.TAST_NOTIFICATION_SERVICE_NAME
  )
  typing.cast(notification_service_pb2_grpc.NotificationServiceStub, stub)
  request = empty_pb2.Empty()
  crosd.log.debug(
      'Invoking notification_service.CloseNotifications with request: %s',
      request,
  )
  stub.CloseNotifications(request)


@tast_service_manager.assert_tast_session_service_alive
def get_all_notifications(
    crosd: 'CrosDevice',
) -> Sequence[notification_service_pb2.Notification]:
  """Gets all the notifications in system tray.

  Args:
    crosd: The CrOS device controller object.

  Returns:
    A list of notifications, each item represents one notification.
  """
  stub = crosd.tast_client.get_or_create_grpc_stub(
      tast_client.TAST_NOTIFICATION_SERVICE_NAME
  )
  typing.cast(notification_service_pb2_grpc.NotificationServiceStub, stub)
  request = empty_pb2.Empty()
  crosd.log.debug(
      'Invoking notification_service.CloseNotifications with request: %s',
      request,
  )
  response = stub.Notifications(request)
  crosd.log.debug(
      'Got response from notification_service.Notifications: %s', response
  )
  return list(response.notifications)


@tast_service_manager.assert_tast_session_service_alive
def wait_for_notification(
    crosd: 'CrosDevice',
    predicates: Sequence[notification_service_pb2.WaitPredicate],
    timeout_sec: int = _WAIT_FOR_NOTIFICATION_DEFAULT_TIMEOUT_SEC,
) -> None:
  """Waits for an eligible notification or throws an Error.

  This will return immediately if there's already an eligible notification.

  Args:
    crosd: The CrOS device controller object.
    predicates: The predicates contain the conditions for querying
      notifications.
    timeout_sec: The timeout to wait.

  Raises:
    NotificationServiceError: If failed to wait for a notification satisfy all
      waiting predicates.
  """
  stub = crosd.tast_client.get_or_create_grpc_stub(
      tast_client.TAST_NOTIFICATION_SERVICE_NAME
  )
  typing.cast(notification_service_pb2_grpc.NotificationServiceStub, stub)
  request = notification_service_pb2.WaitForNotificationRequest(
      predicates=predicates,
      timeout_secs=timeout_sec,
  )
  crosd.log.debug(
      'Invoking notification_service.WaitForNotification with request: %s',
      request,
  )
  try:
    stub.WaitForNotification(request)
  except grpc.RpcError as e:
    # See (internal) for why we need cast here.
    error = cast(grpc.Call, e)
    if _GRPC_ERROR_MSG_NOTIFICATION_DID_NOT_APPEAR in error.details():
      raise NotificationServiceError(
          crosd,
          _ERROR_MSG_NOTIFICATION_DID_NOT_APPEAR.format(request=request),
      ) from e


@tast_service_manager.assert_tast_session_service_alive
def wait_until_notification_gone(
    crosd: 'CrosDevice',
    predicates: Sequence[notification_service_pb2.WaitPredicate],
    timeout_sec: int = _WAIT_FOR_NOTIFICATION_DEFAULT_TIMEOUT_SEC,
) -> None:
  """Wait for all eligible notifications to disappear.

  If there are not notifications that satisfy all the predicates, this will
  return immediately.

  Args:
    crosd: The CrOS device controller object.
    predicates: The predicates contain the conditions for querying
      notifications.
    timeout_sec: The timeout to wait.

  Raises:
    NotificationServiceError: If failed to wait all eligible notifications to
      disappear.
  """
  stub = crosd.tast_client.get_or_create_grpc_stub(
      tast_client.TAST_NOTIFICATION_SERVICE_NAME
  )
  typing.cast(notification_service_pb2_grpc.NotificationServiceStub, stub)
  request = notification_service_pb2.WaitUntilNotificationGoneRequest(
      predicates=predicates,
      timeout_secs=timeout_sec,
  )
  crosd.log.debug(
      'Invoking notification_service.WaitUntilNotificationGone with'
      ' request: %s',
      request,
  )
  try:
    stub.WaitUntilNotificationGone(request)
  except grpc.RpcError as e:
    # See (internal) for why we need cast here.
    error = cast(grpc.Call, e)
    if _GRPC_ERROR_MSG_NOTIFICATION_NOT_GONE in error.details():
      raise NotificationServiceError(
          crosd,
          'There are still notifications that satisfy waiting predicates.',
      ) from e

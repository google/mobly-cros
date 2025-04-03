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

"""The CrOS service for screen recording."""

import logging
import os
import time
import typing
from typing import Any

from mobly import expects
from mobly import logger as mobly_logger
from mobly import runtime_test_info
from mobly import utils
from mobly.controllers.android_device_lib import errors
from mobly.controllers.android_device_lib.services import base_service
from mobly.snippet import errors as mobly_snippet_errors

from google.protobuf import empty_pb2
from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import tast_client
from mobly.controllers.cros.lib.tast_services import test_fission_utils
from tast.cros.services.cros.ui import screen_recorder_service_pb2
from tast.cros.services.cros.ui import screen_recorder_service_pb2_grpc

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any


class Error(errors.ServiceError):
  """Base error type for screen recorder service."""

  SERVICE_TYPE = 'ScreenRecorder'


class VideoFileDoesNotExistError(Error):
  """Raised when the video file doesn't exist on the given device path."""


class TastServerNotRunningError(Error):
  """Raised when this service is running while Tast server has died."""


class CreatingExcerptsWhenNotAliveError(Error):
  """Raised when trying to create excerpts while this service is not alive."""


class FfmpegCompleteMetadataError(Error):
  """Raised if FFmpeg raises an error while processing the video."""


class UnknownVideoFormatError(Error):
  """If got an unknown extension name for the video file to process."""


class ScreenRecorderService(base_service.BaseService):
  """A service for recording screen videos from a CrOS device.

  NOTE: This service must be used together with TastSessionService and
  registered after completing the TastSessionService registration.

  Tast service `ScreenRecorderService` will start a long running process on the
  remote device, and generate the video recording file on the device when
  stopping the long running process. This class will pull the video recording
  file to the host.

  Attributes:
    log: A logger adapted from the CrOS device logger, which adds the identifier
      '[ScreenRecorderService]' to each log line: '<CrosDevice log prefix>
      [ScreenRecorderService] <message>'.
  """

  def __init__(self, device: 'CrosDevice', configs: Any = None) -> None:
    """Initializes the instance of ScreenRecorderService.

    Args:
      device: The CrOS device controller object.
      configs: This config argument is required by the interface of
        `BaseService` and will never be used by the screen recorder service.
    """
    del configs  # Unused
    self._device = device
    self._tast_client: tast_client.TastClient = device.tast_client
    self.log = mobly_logger.PrefixLoggerAdapter(
        self._device.log,
        {
            mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX: (
                '[ScreenRecorderService]'
            )
        },
    )
    self._is_alive: bool = False
    self._final_filename = ''
    self._generated_video_host_paths: list[str] = []

  @property
  def debug_tag(self) -> str:
    """Returns the debug tag of the device controller object."""
    return self._device.debug_tag

  def __repr__(self) -> str:
    return f'<ScreenRecorderService|{self._device.debug_tag}>'

  @property
  def is_alive(self) -> bool:
    """True if the Tast session service is alive; False otherwise."""
    if self._is_alive:
      # Raise error if this service is alive but Tast server died.
      self._assert_tast_server_alive()

    return self._is_alive

  def _get_grpc_service_stub(
      self,
  ) -> screen_recorder_service_pb2_grpc.ScreenRecorderServiceStub:
    stub = self._tast_client.get_or_create_grpc_stub(
        tast_client.TAST_SCREEN_RECORDER_SERVICE_NAME
    )
    return typing.cast(
        screen_recorder_service_pb2_grpc.ScreenRecorderServiceStub, stub
    )

  def start(self) -> None:
    """Starts screen recording process on the CrOS device.

    This function blocks until the screen recording process actually starts.

    Raises:
      Error: If the screen recorder service is already running.
    """
    if self.is_alive:
      raise Error(
          self._device, 'Cannot start again when recording is already running.'
      )

    # Assert tast server is alive before trying to start screen recording
    self._assert_tast_server_alive()
    self._start_screen_recording_remote_process()
    self._is_alive = True

  def _start_screen_recording_remote_process(self):
    """Sends a start request to Tast gRPC service `ScreenRecorderService`."""
    request = screen_recorder_service_pb2.StartRequest()
    self.log.debug('Starting screen recording.')
    stub = self._get_grpc_service_stub()

    # Log start video time and filename to enable test fission to use it to sync
    # with chrome OS log file.
    timestamp = mobly_logger.get_log_file_timestamp()
    self._final_filename = (
        f'cros_video,{self._device.serial},'
        f'{self._device.build_info.board},{timestamp}.webm'
    )
    stub.Start(request, timeout=constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC)
    self.log.info(
        test_fission_utils.generate_video_start_log(
            self._device, self._final_filename, False
        )
    )

  def stop(self) -> None:
    """Stops the screen recording process and pulls the video file to host.

    Raises:
      Error: If the screen recording remote process is not alive.
    """
    if not self.is_alive:
      raise Error(
          self._device,
          'Cannot stop the screen recorder service because it is not alive.',
      )

    video_device_path = self._stop_screen_recording_remote_process()
    self._is_alive = False

    self._handle_recorded_video_artifact(video_device_path)

  def _stop_screen_recording_remote_process(self) -> str:
    """Sends a stop request to Tast gRPC service `ScreenRecorderService`."""
    request = empty_pb2.Empty()
    self.log.debug('Stopping screen recording.')
    stub = self._get_grpc_service_stub()
    response = stub.Stop(
        request, timeout=constants.TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC
    )
    self.log.debug('Screen recording stopped with response: %s', response)
    return response.file_name

  def _handle_recorded_video_artifact(self, video_device_path: str) -> None:
    """Handles the recorded video artifact.

    This function performs following steps:
    1. Pull the video file from the device to host.
    2. If the video file is not empty, complete the metadata of the video file.

    Args:
      video_device_path: The device path of the recorded video artifact.

    Returns:
      The host path of the video artifact.
    """
    utils.create_dir(self._device.log_path)
    timestamp = mobly_logger.get_log_file_timestamp()
    video_filename_ext = os.path.splitext(video_device_path)[1]
    tmp_video_host_path = os.path.join(
        self._device.log_path,
        f'tmp_cros_video,{self._device.serial},{self._device.build_info.board},'
        f'{timestamp}{video_filename_ext}',
    )

    final_video_host_path = os.path.join(
        self._device.log_path, self._final_filename
    )
    self._pull_and_clear_video_artifact(video_device_path, tmp_video_host_path)

    os.rename(tmp_video_host_path, final_video_host_path)
    self._generated_video_host_paths.append(final_video_host_path)

  def _pull_and_clear_video_artifact(
      self, video_device_path: str, video_host_path: str
  ):
    """Pulls the video artifact from the device and clears the device file."""
    if not self._device.ssh.is_file(video_device_path):
      raise VideoFileDoesNotExistError(
          self._device,
          'Cannot pull video artifact from device because no file exists at '
          f'the given device path: "{video_device_path}"',
      )

    self.log.debug(
        'Pulling video recording file from device path(%s) to host path(%s)',
        video_device_path,
        video_host_path,
    )
    self._device.ssh.pull(video_device_path, video_host_path)
    self._device.ssh.rm_file(video_device_path)

  def create_output_excerpts(
      self, test_info: runtime_test_info.RuntimeTestInfo
  ) -> list[Any]:
    """Creates screen recording excerpts and returns the excerpt host paths.

    This moves the generated screen recording videos to the given excerpt
    directory.

    Args:
      test_info: `self.current_test_info` in a Mobly test.

    Returns:
      The list of absolute paths to excerpt files.

    Raises:
      CreatingExcerptsWhenNotAliveError: when trying to create excerpts while
        this service is not alive.
    """
    if not self.is_alive:
      self._create_output_excerpts(test_info)
      raise CreatingExcerptsWhenNotAliveError(
          self._device, 'Cannot create excerpts when the service is not alive.'
      )

    # If the screen recording service is alive now, we should stop this service,
    # create excerpts and then re-start the service.
    # Also even if the stop service process raised an error, it should generate
    # excerpts as long as the generated video list is not empty.
    with expects.expect_no_raises(
        f'Failed to stop ScreenRecorderService "{self.alias}".'
    ):
      self.stop()
    try:
      return self._create_output_excerpts(test_info)
    finally:
      self.start()

  def _create_output_excerpts(
      self, test_info: runtime_test_info.RuntimeTestInfo
  ) -> list[Any]:
    dest_dir_path = test_info.output_path
    utils.create_dir(dest_dir_path)

    excerpt_file_paths: list[str] = []
    generated_video_host_paths = self._generated_video_host_paths
    self._generated_video_host_paths = []

    for old_host_path in generated_video_host_paths:
      file_basename = os.path.basename(old_host_path)
      new_host_path = os.path.join(dest_dir_path, file_basename)
      self.log.debug(
          'Moving video recording file from %s to excerpt path %s',
          old_host_path,
          new_host_path,
      )
      os.rename(old_host_path, new_host_path)
      excerpt_file_paths.append(new_host_path)

    return excerpt_file_paths

  def _assert_tast_server_alive(self):
    """Asserts that the Tast server is alive.

    Raises:
      TastServerNotRunningError: If the Tast server has died.
    """
    try:
      self._tast_client.check_server_proc_running()
    except mobly_snippet_errors.ServerDiedError as e:
      raise TastServerNotRunningError(
          self._device, 'Tast Server process has died unexpectedly.'
      ) from e

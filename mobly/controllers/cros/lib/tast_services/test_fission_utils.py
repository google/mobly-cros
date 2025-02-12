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

"""Utils for Test Fission operations on Mobly's CrOS Device."""

from typing import Any

from mobly.controllers.cros.lib import constants

# Avoid directly importing cros_device, which causes circular dependencies
CrosDevice = Any

# ssh echo time command
ECHO_DEVICE_TIME_COMMAND = 'echo $(date +%Y-%m-%dT%T)${EPOCHREALTIME:10:4}'

# copy chrome log time command
COPY_CROS_LOG_TIME_COMMAND = f'tail -1 {constants.CHROME_LOG_DEVICE_PATH}'


def generate_video_start_log(
    device: 'CrosDevice',
    output_filename: str,
    use_device_time: bool = False,
) -> str:
  """Gets the log when video record start.

  Args:
    device: The CrOS device which records the video.
    output_filename: The output filename of the video.
    use_device_time: Whether to use device echo time as timestamp in Mobly main
      log. This is due to the possible time difference CrOS device log timestamp
      and the CrOS device echo time.

  Returns:
    The log contains video starting time and output filename.
  """
  start_timestamp = device.ssh.execute_command(
      ECHO_DEVICE_TIME_COMMAND
      if use_device_time
      else COPY_CROS_LOG_TIME_COMMAND
  ).split('Z')[0]

  return (
      f'INFO:{str(device.serial)} Start video recording {start_timestamp},'
      f' output filename {output_filename}'
  )

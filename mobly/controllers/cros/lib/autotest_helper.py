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

"""A helper for running autotest scripts on a ChromeOS device.

We are planning to move the autotest things to tast-server approach. Do not
directly use this module.
"""

from __future__ import annotations

import dataclasses
import re
from typing import Optional

from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import ssh as ssh_lib


class TouchscreenSpecParseError(Exception):
  """Error when failed to parse the Touchscreen specs of the CrOS device."""


@dataclasses.dataclass
class TouchscreenSpecs:
  """Touchscreen specification from the CrosDevice."""
  node: str
  x_max: int
  y_max: int


# Python script for querying touchscreen specs using autotest_lib embedded in
# CrOS devices.
_AUTOTEST_SCRIPT_QUERY_TOUCHSCREEN_SPECS = [
    'import common',
    'from autotest_lib.client.bin.input import input_device',
    'from autotest_lib.client.cros.input_playback import input_playback',
    'playback = input_playback.InputPlayback()',
    'playback.find_connected_inputs()',
    "touchscreen_node = playback.devices['touchscreen'].node",
    'tsd = input_device.InputDevice(touchscreen_node)',
    "msg = 'Touchscreen spec: node={}, x_max={}, y_max={}'",
    'print(msg.format(touchscreen_node, tsd.get_x_max(), tsd.get_y_max()))',
]

# The regex pattern for the output of the touchscreen specs query.
_OUTPUT_PATTERN_TOUCHSCREEN_SPEC_QUERY = (
    'Touchscreen spec: node=(?P<node>.*), x_max=(?P<x_max>[0-9]+), '
    'y_max=(?P<y_max>[0-9]+)'
)


def query_touchscreen_specs(ssh: ssh_lib.SSHProxy,
                            query_timeout_sec: int = 10) -> TouchscreenSpecs:
  """Queries the touchscreen specification from the ChromeOS device.

  Args:
    ssh: The ssh connection to the ChromeOS device.
    query_timeout_sec: The time in seconds to wait for the query to finish.

  Returns:
    A dataclass contains the touchscreen specification.

  Raises:
    ssh_lib.ExecuteCommandError: Raised if query failed.
    ssh_lib.RemoteTimeoutError: Raised if the query did not complete in the
      given time.
    TouchscreenSpecParseError: Raised if failed parse the Touchscreen specs of
      the CrOS device.
  """
  autotest_scripts = ';'.join(_AUTOTEST_SCRIPT_QUERY_TOUCHSCREEN_SPECS)
  output = run_auto_test_scripts_as_remote_process(
      ssh, autotest_scripts, query_timeout_sec
  ).wait()
  result = re.search(_OUTPUT_PATTERN_TOUCHSCREEN_SPEC_QUERY, output)
  if result is None:
    raise TouchscreenSpecParseError(
        f'Failed to parse touchscreen specs on device {repr(ssh)}, got output: '
        f'{output}'
    )
  return TouchscreenSpecs(
      node=result.group('node'),
      x_max=int(result.group('x_max')),
      y_max=int(result.group('y_max')),
  )


def run_auto_test_scripts_as_remote_process(
    ssh: ssh_lib.SSHProxy,
    scripts: str,
    timeout: Optional[int] = None) -> ssh_lib.RemotePopen:
  """Starts Python autotest scripts as a remote process on the ChromeOS device.

  Args:
    ssh: The ssh connection to the Chrome OS device.
    scripts: The Python autotest scripts.
    timeout: The time in seconds to wait for the command to finish.

  Returns:
    An object represents the remote process.
  """
  return ssh.start_remote_process(
      f'python3 -c "{scripts}"',
      environment={
          'PYTHONPATH': f'$PYTHONPATH:{constants.PYTHON_PATH_FOR_AUTOTEST}'
      },
      timeout=timeout)

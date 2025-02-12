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

"""Build info collector for a Chrome OS device.

References:
https://chromium.googlesource.com/chromiumos/third_party/autotest/+/refs/heads/main/client/bin/utils.py
"""

from __future__ import annotations
import dataclasses
import re

from mobly.controllers.cros.lib import ssh as ssh_lib

# The board info and CrOS version file.
LSB_RELEASE_FILE = '/etc/lsb-release'
# The memory info file.
MEMORY_INFO = '/proc/meminfo'


@dataclasses.dataclass
class BuildInfo:
  """Build information from the CrosDevice."""

  # ARC Android sdk version.
  android_version: int | None

  # Board name.
  board: str

  # Device type.
  board_type: str

  # ChromeOS release version.
  chrome_os_version: str

  # ChromeOS release major version
  chrome_os_major_version: str

  # Chrome OS device's cpu name.
  cpu_name: str

  # Chrome OS device's firmware version.
  #
  # This will be empty on virtual platforms.
  firmware_version: str

  # Chrome OS device's hardware id.
  #
  # This will be empty on virtual platforms.
  hardware_id: str

  # Chrome OS device's revision.
  #
  # This will be empty on virtual platforms.
  hardware_revision: str

  # Chrome OS device's kernel version.
  kernel_version: str

  # Chrome OS device's max CPU core frequency.
  #
  # This will be 0 on platforms where CPU frequency scaling is not supported
  # (e.g., virtual machines).
  max_cpu_frequency_ghz: float

  # ChromeOS platform name.
  platform: str

  # ChromeOS screen(s) resolution.
  screen_resolution: str

  # Chrome OS device's total memory available in the system in GBytes.
  total_memory_gb: int

  @staticmethod
  def collect(ssh: ssh_lib.SSHProxy) -> BuildInfo:
    """Collects build information from a remote Chrome OS device.

    Args:
      ssh: The ssh connection to the Chrome OS device.

    Returns:
      Build information dataclass.

    Raises:
      ssh.RemotePathDoesNotExistError: Info file is not found on Chromebook.
      ssh.ExecuteCommandError: ssh command encounters an error.
    """
    lsb_info = ssh.get_remote_file_contents(LSB_RELEASE_FILE)
    lsb_property = lambda key: _get_board_property(lsb_info, key)
    get_cpu_name = lambda: _get_cpu_name(ssh)
    get_max_cpu_frequency_ghz = lambda: _get_max_cpu_frequency_ghz(ssh)
    get_total_memory_gb = lambda: _get_total_memory_gb(ssh)
    get_command_out = lambda cmd, err=False: _get_command_output(ssh, cmd, err)

    android_version = lsb_property('CHROMEOS_ARC_ANDROID_SDK_VERSION')
    return BuildInfo(
        # Parses lsb file
        android_version=int(android_version) if android_version else None,
        board=lsb_property('BOARD'),
        board_type=lsb_property('DEVICETYPE'),
        chrome_os_version=lsb_property('CHROMEOS_RELEASE_VERSION'),
        chrome_os_major_version=lsb_property(
            'CHROMEOS_RELEASE_CHROME_MILESTONE'),

        # Parses command output
        cpu_name=get_cpu_name(),
        total_memory_gb=get_total_memory_gb(),
        max_cpu_frequency_ghz=get_max_cpu_frequency_ghz(),
        platform=get_command_out('cros_config / name'),
        firmware_version=get_command_out('crossystem fwid', err=True),
        hardware_id=get_command_out('crossystem hwid', err=True),
        hardware_revision=get_command_out('mosys platform version', err=True),
        kernel_version=get_command_out('uname -r'),
        screen_resolution=get_command_out(
            'for f in /sys/class/drm/*/*/modes; do head -1 $f; done'),
    )


def _get_board_property(lsb_release_info: str, key: str) -> str:
  match = re.search(rf'{key}=(.*)', lsb_release_info)
  return match.group(1) if match else ''


def _get_command_output(ssh: ssh_lib.SSHProxy,
                        command: str,
                        ignore_error: bool = False) -> str:
  return ssh.execute_command(command, timeout=10, ignore_error=ignore_error)


def _get_cpu_name(ssh: ssh_lib.SSHProxy) -> str:
  # Try get cpu name from device tree first
  if ssh.exists('/proc/device-tree/compatible'):
    return _get_command_output(
        ssh, 'sed -e \'s/\\x0/\\n/g\' '
        '/proc/device-tree/compatible | tail -1').replace(',', ' ')

  # Get cpu name from uname -p
  ret = _get_command_output(ssh, 'uname -p')

  # 'uname -p' return variant of unknown or amd64 or x86_64 or i686
  # Try get cpu name from /proc/cpuinfo instead
  if re.match('unknown|amd64|[ix][0-9]?86(_64)?', ret, re.IGNORECASE):
    ret = _get_command_output(
        ssh, 'grep model.name /proc/cpuinfo | cut -f 2 -d: | head -1')

  # Remove bloat from CPU name, for example
  # 'Intel(R) Core(TM) i5-7Y57 CPU @ 1.20GHz'-> 'Intel Core i5-7Y57'
  # 'Intel(R) Xeon(R) CPU E5-2690 v4 @ 2.60GHz'-> 'Intel Xeon E5-2690 v4'
  # 'AMD A10-7850K APU with Radeon(TM) R7 Graphics'-> 'AMD A10-7850K'
  # 'AMD GX-212JC SOC with Radeon(TM) R2E Graphics'-> 'AMD GX-212JC'
  trim_re = r' (@|processor|apu|soc|radeon).*|\(.*?\)| cpu'
  return re.sub(trim_re, '', ret, flags=re.IGNORECASE)


def _get_max_cpu_frequency_ghz(ssh: ssh_lib.SSHProxy) -> float:
  max_freq_info = _get_command_output(
      ssh, 'ls /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_max_freq | '
      'xargs cat')
  if not max_freq_info:
    return 0.0
  max_cpu_frequency = max(list(map(int, max_freq_info.split('\n'))))
  # Convert frequency to GHz with 1 digit accuracy after the decimal point.
  return int(round(max_cpu_frequency * 1e-5)) * 0.1


def _get_total_memory_gb(ssh: ssh_lib.SSHProxy) -> int:
  memory_info = ssh.get_remote_file_contents(MEMORY_INFO)
  match = re.search(r'MemTotal: *(\d+) kB', memory_info)
  return int(match.group(1)) // (1024 * 1024) if match else 0

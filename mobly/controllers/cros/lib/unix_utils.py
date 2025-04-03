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

"""Convenience functions to deal with unix commands.

References:
https://chromium.googlesource.com/chromiumos/third_party/autotest/+/refs/heads/main/client/bin/utils.py
"""

from collections.abc import Callable
from typing import Optional

ShellType = Callable[[str], str]


def get_oldest_by_name(shell: ShellType,
                       name: str) -> tuple[Optional[int], Optional[str]]:
  """Returns pid and command line of oldest process whose name matches |name|.

  Args:
    shell: The target shell to execute the query.
    name: egrep expression to match desired process name.

  Returns:
    A tuple of (pid, command_line) of the oldest process whose name matches
    |name|.
  """
  pid = get_oldest_pid_by_name(shell, name)
  if pid:
    command_line = shell(f'ps -p {pid} -o command=').strip()
    return pid, command_line

  return None, None


def get_oldest_pid_by_name(shell: ShellType, name: str) -> Optional[int]:
  """Returns the oldest pid of a process whose name perfectly matches |name|.

  name is an egrep expression, which will be matched against the entire name
  of processes on the system.  For example:

    get_oldest_pid_by_name('chrome')

  on a system running
    8600 ?        00:00:04 chrome
    8601 ?        00:00:00 chrome
    8602 ?        00:00:00 chrome-sandbox

  would return 8600, as that's the oldest process that matches.
  chrome-sandbox would not be matched.

  Args:
    shell: The target shell to execute the query.
    name: egrep expression to match. Will be anchored at the beginning and end
      of the match string.

  Returns:
    pid as an integer, or None if one cannot be found.
  """
  str_pid = shell(f'pgrep -o ^{name}$').strip()
  return int(str_pid) if str_pid else None

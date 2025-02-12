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

"""A sample test demonstrating using Mobly CrOS controller."""

from mobly import base_test
from mobly import test_runner

from mobly.controllers.cros import cros_device


class HelloWorldTest(base_test.BaseTestClass):
  """A sample test demonstrating using Mobly CrOS controller."""

  def setup_class(self):
    super().setup_class()
    # Registers cros_device controller module. By default, we expect at
    # least one CrOS device.
    self._crosd = self.register_controller(cros_device)[0]

  def test_ssh_execute_command(self):
    # Executes console command 'ls' on the CrOS device and gets the result.
    result = self._crosd.ssh.execute_command('ls')
    self._crosd.log.info('ls result: %s', result)


if __name__ == '__main__':
  test_runner.main()

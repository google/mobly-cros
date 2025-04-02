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

"""Examples for advanced features in the Mobly CrOS module."""

import time

from mobly import asserts
from mobly import base_test
from mobly import test_runner

from mobly.controllers.cros import cros_device
from mobly.controllers.cros.lib.tast_services import device_log_service
from mobly.controllers.cros.lib.tast_services import screen_recorder_service
from mobly.controllers.cros.lib.tast_services import tast_session_service
from tast.cros.services.cros.ui import automation_service_pb2


class AdvancedFeaturesExampleTest(base_test.BaseTestClass):
  """Examples for advanced features in the Mobly CrOS module."""

  _crosd: cros_device.CrosDevice

  def setup_class(self):
    super().setup_class()
    self._crosd = self.register_controller(cros_device)[0]

    log_service_config = device_log_service.Config(
        log_types={
            device_log_service.LogType.CHROME_LOG,
            device_log_service.LogType.BLUETOOTH_MONITOR,
        })
    self._crosd.services.register('device_log_service',
                                  device_log_service.DeviceLogService,
                                  log_service_config)

    login_config = tast_session_service.Config(
        # Note that keep_state=False will delete user data on the CrOS device.
        # We recommend this setting as it helps us avoid test flakiness due to
        # device state
        keep_state=False)
    self._crosd.services.register('tast_session_service',
                                  tast_session_service.TastSessionService,
                                  login_config)

    # Note that screen recorder can only be used after the tast_session_service
    # is registered and started successfully.
    self._crosd.services.register('screen_recorder_service',
                                  screen_recorder_service.ScreenRecorderService)

  def teardown_test(self):
    self._crosd.services.create_output_excerpts_all(self.current_test_info)

  def test_keyboard_input_example(self):
    # Input hotkey "Ctrl"+"t" to open the Chrome browser on CrOS device
    self._crosd.input_hotkey('Ctrl+t')

    # Input the given hotkey to get the cursor to the address bar of the browser
    self._crosd.input_hotkey('Alt+d')

    # Input the given text in the address bar
    self._crosd.input_text('Test Type Successfully.')

  def test_webdriver_example(self):
    # Open the Chrome browser
    self._crosd.input_hotkey('Ctrl+t')

    # Navigate to the setting page
    self._crosd.webdriver.get('chrome://os-settings')

    # Execute a JS script to click on the button "About Chrome OS"
    self._crosd.webdriver.execute_script(
        'return document'
        '.querySelector("os-settings-ui").shadowRoot'
        '.querySelector("os-settings-menu").shadowRoot'
        '.querySelector("#aboutItem")').click()

  def test_reboot(self):
    self._crosd.input_hotkey('Ctrl+t')
    self._crosd.input_text('Before reboot.')

    self._crosd.reboot()

    self._crosd.input_hotkey('Ctrl+t')
    self._crosd.input_text('After reboot.')

  def test_suspension(self):
    self._crosd.input_hotkey('Ctrl+t')
    self._crosd.input_text('Before suspension.')

    self._crosd.suspend(suspend_for_sec=5)

    self._crosd.input_hotkey('Ctrl+t')
    self._crosd.input_text('After suspension.')

  def test_tast_uiauto(self):
    # Get the initial UI Tree.
    request = automation_service_pb2.GetUITreeRequest()
    response = self._crosd.services.automation_service_wrapper.invoke_grpc_call(
        'GetUITree', request
    )
    self._crosd.log.info('Initial UI tree: %s', response.ui_tree)

    # Click to expand the calendar tray in the lower right corner of the screen.
    click_request = automation_service_pb2.LeftClickRequest()
    click_request.finder.node_withs.add().first = True
    click_request.finder.node_withs.add().name_containing = 'Calendar'
    self._crosd.log.info(
        'Triggering Tast UIAuto LeftClick with request: %s', click_request
    )
    self._crosd.services.automation_service_wrapper.invoke_grpc_call(
        'LeftClick', click_request
    )
    time.sleep(3)

    # Get current UI tree.
    request = automation_service_pb2.GetUITreeRequest()
    response = self._crosd.services.automation_service_wrapper.invoke_grpc_call(
        'GetUITree', request
    )
    self._crosd.log.info(
        'UI tree after click calendar view: %s', response.ui_tree
    )

    # Check that the expected node exists.
    exist_request = automation_service_pb2.IsNodeFoundRequest()
    exist_request.finder.node_withs.add().first = True
    exist_request.finder.node_withs.add().name = 'Calendar'
    exist_request.finder.node_withs.add().role = (
        automation_service_pb2.Role.ROLE_STATIC_TEXT
    )
    self._crosd.log.info(
        'Triggering Tast UIAuto IsNodeFound with request: %s', exist_request
    )
    exist_response = (
        self._crosd.services.automation_service_wrapper.invoke_grpc_call(
            'IsNodeFound', exist_request
        )
    )
    self._crosd.log.info('Tast UIAuto IsNodeFound response: %s', exist_response)

    asserts.assert_true(exist_response.found, 'Expected node not found.')


if __name__ == '__main__':
  test_runner.main()

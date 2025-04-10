# Mobly ChromeOS Controller

Mobly ChromeOS controller module for using Python code to operate ChromeOS
(CrOS) devices in Mobly tests.

This is not an officially supported Google product. This project is not eligible
for the
[Google Open Source Software Vulnerability Rewards Program](https://bughunters.google.com/open-source-security).

## Requirements

-   Python 3.11+
-   Mobly 1.12.4+

## Hardware Requirements

1.  One or more ChromeOS devices (that are being tested).
1.  A Linux workstation (host machine) to run Mobly test script.

## Set Up ChromeOS Devices

To control the ChromeOS device, users need to do some one-time settings on the
ChromeOS device.

Pre-setting requirements:

-   [Flash a test image to ChromeOS device](https://www.chromium.org/chromium-os/developer-library/reference/tools/cros-flash/)
    (prefer to use latest build).
-   Connect the ChromeOS device to the same local network as the host machine
    (your workstation).

## Use ChromeOS Devices in a test

This section introduces how to develop a basic Mobly ChromeOS controller test
which runs one shell command on the ChromeOS device.

### Define a Testbed

Define the ChromeOS device in a testbed with CrosDevice type. Save the config in
a local Mobly config yaml file. Example Testbed config:

**sample_config.yaml**

```yaml
TestBeds:
- Name: SampleCrosTestbed
  Controllers:
    CrosDevice:
      - hostname: "DEVICE_IP"
```

### Write Test Script

We use the "Hello World" test script as a simple example using ChromeOS device.
In this example, we will connect to a ChromeOS device and execute a shell
command on this ChromeOS device. Mobly test script:

**hello_world_test.py**

```python
"""A sample test demonstrating using Mobly Cros controller."""

from mobly import base_test
from mobly import test_runner

from mobly.controllers.cros import cros_device


class HelloWorldTest(base_test.BaseTestClass):
  """A sample test demonstrating using Mobly ChromeOS controller."""

  def setup_class(self):
    super().setup_class()
    # Registers cros_device controller module. By default, we expect at
    # least one ChromeOS device.
    self._crosd = self.register_controller(cros_device)[0]

  def test_ssh_execute_command(self):
    # Executes console command 'ls' on the ChromeOS device and gets the result.
    result = self._crosd.ssh.execute_command('ls')
    self._crosd.log.info('ls result: %s', result)


if __name__ == '__main__':
  test_runner.main()
```

### Run Test

```shell
python hello_world_test.py -c sample_config.yaml
```

## ChromeOS Device Login

Mobly ChromeOS controller provides the TastSessionService for tests to start a
new Chrome user session with the given account and password. You should register
it on CrosDevice objects:

```python
from mobly import base_test

from mobly.controllers.cros import cros_device
from mobly.controllers.cros.lib.tast_services import tast_session_service

class MoblyTastExampleTest(base_test.BaseTestClass):

  _crosd: cros_device.CrosDevice

  def setup_class(self):
    super().setup_class()
    self._crosd = self.register_controller(cros_device)[0]

    login_config = tast_session_service.Config(
        # Note that keep_state=False will delete user data on the ChromeOS device.
        # We recommend this setting as it helps us avoid test flakiness due to
        # device state.
        keep_state=False,
    )
    self._crosd.services.register('tast_session_service',
                                  tast_session_service.TastSessionService,
                                  login_config)
```

Regarding the login config,

-   If your test doesn't require any account information, use the above config
    and the ChromeOS device will log in with a default test account. If your
    test requires logging in with specific account, e.g. pairing a ChromeOS
    device and an Android device logged in with the same account, you need to
    log in with an OTA account and following login config:

```python
login_config = tast_session_service.Config(
    # GAIA login mode uses a GAIA backend to verify the login credential,
    # which could be slow and sometimes flaky, use this mode only when you
    # really need it.
    login_mode=tast_session_service.LOGIN_MODE_GAIA_LOGIN,
    username="xxxx",
    password="xxxxxxx",
    keep_state=False,
)
```

### Set logging levels

TastSessionService supports passing extra command line flags to Chrome. This is
mostly used for setting logging levels. Here's an example usage:

```python
login_config = tast_session_service.Config(
    ...,
    extra_args=[
        '--enable-logging',
        # "ble_*=3" sets the VLOG level of files prefixed with "ble_" to 3
        '--vmodule=ble_*=3,*blue*=3,device_event_log*=3',
        # Sets the VLOG level of other files to be 1
        '--v=1',
    ]
)
```

You can check that the flags are properly passed by checking chrome://version
tab on the ChromeOS device. See
[doc](https://www.chromium.org/for-testers/enable-logging/) for more details
about ChromeOS logging.

### Change ChromeOS feature flags

TastSessionService supports enabling/disabling ChromeOS features. Instead of
modifying feature flags via the chrome://flags page and then restarting Chrome,
you only need to modify the login config, the features will be enabled/disabled.
Here's an example:

```python
login_config = tast_session_service.Config(
    ...,
    enable_features=['EcheSWA', 'FastPair'],
    disable_features=['EcheSWADebugMode'],
    ...
)
```

### Device Language Setting

Some automation tools requires English as the system language. In the login
config, we have set region='US' which asks the ChromeOS device to use English.

## Device Log Collection

This section describes using DeviceLogService to get logs on ChromeOS devices,
which are critical for debugging tests. Here's an example which collects the
chrome log /var/log/chrome/chrome and bluetooth monitor log from ChromeOS
devices.

```python
from mobly.controllers.cros.lib.tast_services import device_log_service

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
```

Currently ChromeOS logs are scattered in different places, and different logs
need to be obtained in different ways. So we need to increase the supported log
types one by one. The supported log types can be found in LogType.

## Screen Recording

Screen recording can be critical for debugging tests that involve UI.

Mobly ChromeOS controller provides the ScreenRecorderService to record the
screen on ChromeOS devices. You should register it on CrosDevice objects:

```python
from mobly.controllers.cros.lib.tast_services import screen_recorder_service
...

def setup_class(self):
  ...
  self._crosd.services.register('tast_session_service',
                                tast_session_service.TastSessionService,
                                login_config)

  # ScreenRecorderService can only be registered after TastSessionService
  self._crosd.services.register('screen_recorder_service',
                                screen_recorder_service.ScreenRecorderService)
```

## Keyboard Input Control

The CrosDevice provides two interfaces to control keyboard input:

-   input_text: Inputs text on the test device by simulating typing on the
    keyboard.
-   input_hotkey: Inputs the hotkey by simulating key events on the keyboard.

Here's an example:

```python
  def test_keyboard_input_example(self):
    # Input hotkey "Ctrl"+"t" to open the Chrome browser on ChromeOS device
    self._crosd.input_hotkey('Ctrl+t')

    # Input the given hotkey to get the cursor to the address bar of the browser
    self._crosd.input_hotkey('Alt+d')

    # Input the given text in the address bar
    self._crosd.input_text('Test Type Successfully.')
```

## Webdriver

[Webdriver](https://www.selenium.dev/documentation/webdriver/) is an open-source
control mechanism that enables remote control of web browsers.

Mobly ChromeOS controller creates a helper module for setting up and tearing
down a remote Webdriver object, so users can use this object to operate the
Chrome browser on ChromeOS devices, like navigating pages and calling JavaScript
APIs to access the underlying HTML UI elements.

Here is an example:

```python
  def test_webdriver_example(self):
    # Open the Chrome browser
    self._crosd.input_hotkey('Ctrl+t')

    # Navigate to the setting page
    self._crosd.webdriver.get('chrome://os-settings')

    # Execute a JS script to click on the button "About ChromeOS"
    self._crosd.webdriver.execute_script(
        'return document'
        '.querySelector("os-settings-ui").shadowRoot'
        '.querySelector("os-settings-menu").shadowRoot'
        '.querySelector("#aboutItem")').click()
```

## Tast services

[`Tast`](https://github.com/google/mobly-cros/tree/main/tast) folder contain all generated files with services required for CrOS controller. 

To update or regenerate services follow [`scripts/README`](https://github.com/google/mobly-cros/tree/main/scripts/README)

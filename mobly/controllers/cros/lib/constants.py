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

"""Constants for the Chrome OS controller related modules."""

import os

# Chrome OS test image ssh username and password.
SSH_USERNAME = 'root'
SSH_PASSWORD = 'test0000'

# Remote folder that stores Chrome binary.
CHROME_LOCATION = '/opt/google/chrome'

# Use default user_data directory on CrOS.
# On CrOS, Chrome session is started when we are logging in and is not started
# by chromedriver (which has the ability to set custom user data directory).
# So changing it to custom directory will have no effect.
USER_DATA_LOCATION = '/home/chronos'

# User home directory on CrOS.
USER_HOME_LOCATION = '/home/chronos/user/MyFiles'

# Crash data location.
CRASH_DATA_LOCATION = os.path.join(USER_DATA_LOCATION, 'crash')

# Chrome executable binary location.
CHROME_BINARY_LOCATION = os.path.join(CHROME_LOCATION, 'chrome')

# Chrome debug logs location.
CHROME_LOG = '/var/log/chrome/chrome'

# Chrome driver binary on CrOS.
CHROME_DRIVER_EXE_PATH = '/usr/local/chromedriver/chromedriver'

# Chrome driver debug logs location.
CHROME_DRIVER_LOG = '/var/log/chromedriver.log'

# Python "autotest" lib path on CrOS.
PYTHON_PATH_FOR_AUTOTEST = '/usr/local/autotest/bin'

# Tast server binary on CrOS.
TAST_SERVER_EXE_PATH = '/usr/local/libexec/tast/bundles/local/cros'

# Timeout seconds for terminating the Tast server
TAST_SERVER_TERMINATE_TIMEOUT_SEC = 30

# Timeout seconds for connecting to the Tast server
TAST_SERVER_CONNECTION_TIMEOUT_SEC = 60

# Default timeout seconds for sending a gRPC call to Tast gRPC server
TAST_GRPC_CALL_DEFAULT_TIMEOUT_SEC = 60 * 10

# The device path of the Chrome log
CHROME_LOG_DEVICE_PATH = '/var/log/chrome/chrome'

# The device path of the CrOS network log
NET_LOG_DEVICE_PATH = '/var/log/net.log'

# The device path of the CrOS messages
MESSAGES_LOG_DEVICE_PATH = '/var/log/messages'

# The URL of opening a new tab in Chrome
NEW_CHROME_TAB_URL = 'chrome://newtab'

# The attribute name in service manager reserved for SnippetManagementService
SNIPPET_MANAGEMENT_SERVICE_NAME = 'snippets'

# The gRPC server logs of Floss pandora server.
FLOSS_PANDORA_SERVER_LOG = '/var/log/grpc_server_log'

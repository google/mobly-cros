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

"""Controller configurations for the Chrome OS controller module."""

from __future__ import annotations

from collections.abc import Mapping
import dataclasses
import json
import logging
from typing import Any

import dacite

from mobly.controllers.cros.lib import constants

_CROS_DEVICE_CONFIG_MISSING_REQUIRED_KEY_MSG = 'Missing required key in config'
_CROS_DEVICE_CONFIG_INVALID_VALUE_MSG = 'Invalid value in config'


class Error(Exception):
  """Raised for errors during the controller configs parsing."""


def _convert_to_dict_if_json(data: Any) -> Any:
  """Converts the input data to a dict if the it is valid JSON string."""
  if isinstance(data, str):
    try:
      return json.loads(data)
    except json.decoder.JSONDecodeError:
      pass
  return data


# The key of dimension field in the raw controller config.
_RAW_CONTROLLER_CONFIG_KEY_DIMENSION = 'dimensions'


def _transform_raw_controller_config(
    config_data_class: type[object],
    key_custom_configs: str,
    config: dict[str, Any],
) -> dict[str, Any]:
  """Transforms the raw controller configs.

  This function divides the config items into known items and unknown items
  according to the given data class. Known items are config fields declared in
  the data class, others are unknown fields.

  For more details about the logic of this function, please look at the
  following example:

  ```
  class ExampleDeviceConfig:
    hostname: str
    gaia_email: str
    gaia_password: str
    custom_configs: Mapping[str, Any]

  input config:
  {
    'hostname': '172.16.243.238',
    'unknown_key_1': 'val_1',
    'dimensions': {
      'gaia_email: 'test@gmail.com',
      'gaia_password': 'password',
      'unknown_key_2': 'val_2',
    }
    'custom_configs': {
      'unknown_key_3': 'val_3',
    }
  }

  transformed config:
  {
    'hostname': '172.16.243.238',
    'gaia_email: 'test@gmail.com',
    'gaia_password': 'password',
    'custom_configs': {
      'property_unknown_key_1': 'val_1',
      'dimension_unknown_key_2': 'val_2',
      'unknown_key_3': 'val_3',
    }
  }
  ```

  The given data class must have a field to store unknown config items, which is
  `custom_configs` in the above example. `hostname`, `gaia_email`, and
  `gaia_password` are for known config items.

  For the input configs, this function extracts known fields from the top level
  config items and config items under `input_config['dimensions']`.
  Other config items in input configs are regarded as unknown config items,
  this function adds the prefix "property_" or "dimension_" to them and
  store them under `output_config['custom_configs']`. Config items in
  `input_configs['custom_configs']` (if exist) are preserved as is. If
  key conflicts occur, the priority of overwriting is:

    "top level items" > "items in dimensions" > "items in custom configs"

  Args:
    config_data_class: The data class used for transforming the given config.
    key_custom_configs: The key of the custom config field in the data class.
    config: The raw controller configs to be transformed.

  Returns:
    Transformed configs.

  Raises:
    ValueError: If got invalid arguments.
  """
  if not dataclasses.is_dataclass(config_data_class):
    raise ValueError(
        'Argument "config_data_class" must be a dataclass. Got:'
        f' {config_data_class}'
    )

  known_field_keys = set(
      field.name for field in dataclasses.fields(config_data_class)
  )
  if key_custom_configs not in known_field_keys:
    raise ValueError(
        'Argument "key_custom_configs" must be the one field of the given data'
        f' class {config_data_class}. Got: {key_custom_configs}'
    )

  new_config = {}
  new_config[key_custom_configs] = {}

  # Handle original custom configs.
  if original_custom_config := config.get(key_custom_configs):
    if isinstance(original_custom_config, dict):
      new_config[key_custom_configs] = original_custom_config
    else:
      logging.warning(
          (
              'The "custom_configs" field in original controller config is'
              ' ignored, which is expected to be a dict while got: %s'
          ),
          original_custom_config,
      )

  # Handle config items under the dimensions field.
  if original_dimensions := config.get(
      _RAW_CONTROLLER_CONFIG_KEY_DIMENSION, {}
  ):
    if isinstance(original_dimensions, dict):
      for key, value in config.get(
          _RAW_CONTROLLER_CONFIG_KEY_DIMENSION, {}
      ).items():
        if key in known_field_keys:
          new_config[key] = value
        else:
          new_config[key_custom_configs][f'dimension_{key}'] = value
    else:
      logging.warning(
          (
              'The "dimensions" field in original controller config is ignored,'
              ' which is expected to be a dict while got: %s'
          ),
          original_dimensions,
      )

  # Handle top level config items in raw controller config.
  for key, value in config.items():
    if key in (_RAW_CONTROLLER_CONFIG_KEY_DIMENSION, key_custom_configs):
      continue

    if key in known_field_keys:
      new_config[key] = value
    else:
      new_config[key_custom_configs][f'property_{key}'] = value

  return new_config


@dataclasses.dataclass
class CrosDeviceConfig:
  """Provides configs and default values for CrosDevice."""

  # The IP address or hostname of the test machine.
  hostname: str

  # Username to log the device in.
  gaia_email: str | None = None

  # Password to log the device in.
  gaia_password: str | None = None

  # The SSH port of the test machine.
  custom_ssh_port: int = 22

  # The port on the local machine for ssh port forwarding.
  custom_ssh_forward_port: int = 0

  # The SSH username of the test machine. If not specified, it will use the
  # default username.
  custom_ssh_username: str = constants.SSH_USERNAME

  # The SSH password of the test machine.
  # If not specified default SSH key will be used.
  custom_ssh_password: str | None = None

  # If True, Mobly will remove root filesystem verification on this CrOS device.
  # Nothing will happen if the verification has been removed.
  remove_rootfs_verification: bool = False

  # The field for storing custom configs.
  custom_configs: Mapping[str, Any] = dataclasses.field(default_factory=dict)

  @classmethod
  def from_dict(cls, configs: dict[str, Any]) -> CrosDeviceConfig:
    """Parses controller configs from Mobly runner to CrosDeviceConfig.

    This will divide the config items in the given `configs` dict into known
    items and unknown items. Known items are fields declared in this data class,
    unknown items will be stored in the field `custom_configs`. Here's an
    example:

    ```
    input configs:
    {
      'hostname': '172.16.243.238',
      'unknown_key_1': 'val_1',
      'dimensions': {
        'gaia_email: 'test@gmail.com',
        'unknown_key_2': 'val_2',
      }
      'custom_configs': {
        'unknown_key_3': 'val_3',
      }
    }

    output:
    CrosDeviceConfig(
        hostname='172.16.243.238',
        gaia_email='test@gmail.com',
        custom_configs={
            'property_unknown_key_1': 'val_1',
            'dimension_unknown_key_2': 'val_2',
            'unknown_key_3': 'val_3',
        }
    )
    ```

    For more details about the config transformation logic, please refer to
    the docstring of `_transform_raw_controller_config`.

    Args:
      configs: A dictionary of string parameters.

    Returns:
      CrosDeviceConfig data class.
    """
    type_converters = {
        # Integer converter: any integer value in string
        # simply cast it to integer.
        int: int,
    }

    key_custom_configs = 'custom_configs'

    if (custom_configs := configs.get(key_custom_configs)) is not None:
      configs[key_custom_configs] = _convert_to_dict_if_json(custom_configs)

    configs = _transform_raw_controller_config(
        CrosDeviceConfig, key_custom_configs, configs
    )
    try:
      return dacite.from_dict(
          data_class=CrosDeviceConfig,
          data=configs,
          config=dacite.Config(type_hooks=type_converters),
      )
    except dacite.exceptions.MissingValueError as err:
      raise Error(
          f'{_CROS_DEVICE_CONFIG_MISSING_REQUIRED_KEY_MSG}: {configs}'
      ) from err
    except ValueError as err:
      raise Error(
          f'{_CROS_DEVICE_CONFIG_INVALID_VALUE_MSG}: {configs}'
      ) from err

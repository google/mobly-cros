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

"""The CrOS service for streaming multiple device logs to the host."""

from collections.abc import Set
import dataclasses
import enum
import pathlib
import signal
from typing import Optional, Any

from mobly import logger as mobly_logger
from mobly import runtime_test_info
from mobly import utils
from mobly.controllers.android_device_lib.services import base_service

from mobly.controllers.cros.lib import file_clipper
from mobly.controllers.cros.lib import constants
from mobly.controllers.cros.lib import ssh as ssh_lib

# Avoid directly importing cros_device, which causes circular dependencies.
CrosDevice = Any

# The interval time for periodically printing memory usage.
MEMORY_USAGE_DUMP_INTERVAL_SEC = 60


class ConfigError(Exception):
  """Raised when received an invalid config."""


class _RemoteCommandOutputCollector:
  """The class for executing a remote command on device and collecting output.

  This class is responsible for two things:
  * Executes a remote process on the device and streams its output to the host.
  * Supports per-test excerpts generation.

  Note that even though this can start and stop the remote process multiple
  times, this will stream the command output to the same host file, and the
  create excerpts based on that host file.
  """

  def __init__(self, ssh: ssh_lib.SSHProxy, log_host_dir: pathlib.Path,
               command: str, excerpt_tag: str) -> None:
    """Initializes an instance.

    Args:
      ssh: The ssh proxy to execute the remote command.
      log_host_dir: The host directory to save the output of the remote command.
      command: The remote command to execute.
      excerpt_tag: The tag that will be contained in the output file name.
    """
    self._ssh = ssh
    self._command = command
    self._excerpt_tag = excerpt_tag
    self._proc = None

    self._host_file_path = pathlib.Path(log_host_dir, f'{excerpt_tag}.log')
    self._file_clipper = file_clipper.FileClipper(self._host_file_path)

  def __del__(self) -> None:
    self._file_clipper.close()

  @property
  def is_alive(self) -> bool:
    """True if the collector is alive; False otherwise."""
    return self._proc is not None and self._proc.poll() is None

  @property
  def excerpt_tag(self) -> str:
    """The tag that will be contained in the output file name."""
    return self._excerpt_tag

  def start_remote_process(self) -> None:
    """Starts the remote process and streams the output to a host file."""
    self._proc = self._ssh.start_remote_process(
        self._command, get_pty=True, output_file_path=str(self._host_file_path))

  def stop_remote_process(self) -> None:
    """Stops the remote process and output stream."""
    if not self.is_alive:
      return

    if self._proc:
      self._proc.send_signal(signal_id=signal.SIGTERM, timeout=10)
    self._proc = None

  def create_output_excerpts(self, excerpt_file_path: pathlib.Path) -> None:
    """Creates excerpts of the output of the remote command."""
    self._file_clipper.clip_new_content(excerpt_file_path)


class LogType(enum.Enum):
  """The enumeration of supported log types."""

  # The Chrome log /var/log/chrome/chrome
  CHROME_LOG = 1

  # The Bluetooth monitor log produced by command `btmon`
  BLUETOOTH_MONITOR = 2

  # Periodically print the memory usage and the processes with the largest
  # memory usage.
  MEMORY_USAGE = 3

  # The logs of Floss pandora server.
  FLOSS_PANDORA_SERVER_LOG = 4

  # The ChromeOS Network log /var/log/net.log
  NET_LOG = 5

  # The ChromeOS Messages log /var/log/messages
  MESSAGES_LOG = 6


@dataclasses.dataclass
class Config:
  """A configuration object for configuring device log service.

  See DeviceLogService's docstring for an example usage.

  Attributes:
    log_types: The logs to be streamed from the testing device to host.
    memory_usage_top_n_process: The number of processes whose memory usage needs
      to be printed, sorted by memory usage from high to low. This config only
      takes effect when the log `LogType#MEMORY_USAGE` is streamed.
  """

  log_types: Set[LogType] = dataclasses.field(
      default_factory=lambda: {LogType.CHROME_LOG, LogType.BLUETOOTH_MONITOR})

  memory_usage_top_n_process: int = 10

  def create_log_collectors(
      self, ssh: ssh_lib.SSHProxy,
      log_host_dir: pathlib.Path) -> list[_RemoteCommandOutputCollector]:
    """Creates log collectors based on the configured log types.

    Args:
      ssh: The ssh proxy.
      log_host_dir: The host directory to save the output of the remote command.

    Returns:
      The created log collectors.

    Raises:
      ConfigError: If got unknown log type.
    """
    log_collectors = []
    for log_type in self.log_types:
      log_collectors.append(
          self._create_log_collector(log_type, ssh, log_host_dir))
    return log_collectors

  def _create_log_collector(
      self, log_type: LogType, ssh: ssh_lib.SSHProxy,
      log_host_dir: pathlib.Path) -> _RemoteCommandOutputCollector:
    """Creates a log collector based on the given log type enumeration."""
    if log_type == LogType.CHROME_LOG:
      return _RemoteCommandOutputCollector(
          ssh,
          log_host_dir,
          command=f'tail -F -n 0 {constants.CHROME_LOG_DEVICE_PATH}',
          excerpt_tag='chrome')
    if log_type == LogType.NET_LOG:
      return _RemoteCommandOutputCollector(
          ssh,
          log_host_dir,
          command=f'tail -F -n 0 {constants.NET_LOG_DEVICE_PATH}',
          excerpt_tag='net',
      )
    if log_type == LogType.MESSAGES_LOG:
      return _RemoteCommandOutputCollector(
          ssh,
          log_host_dir,
          command=f'tail -F -n 0 {constants.MESSAGES_LOG_DEVICE_PATH}',
          excerpt_tag='messages',
      )
    if log_type == LogType.BLUETOOTH_MONITOR:
      return _RemoteCommandOutputCollector(
          ssh, log_host_dir, command='btmon', excerpt_tag='btsnoop')

    if log_type == LogType.FLOSS_PANDORA_SERVER_LOG:
      return _RemoteCommandOutputCollector(
          ssh,
          log_host_dir,
          command=f'tail -F -n 0 {constants.FLOSS_PANDORA_SERVER_LOG}',
          excerpt_tag='floss_pandora_server')

    if log_type == LogType.MEMORY_USAGE:
      # Due to the output format of `top` command, we need "+ 6" here, i.e.
      # keep the first "n + 6" lines if we need the information of the first "n"
      # processes.
      keep_first_n_lines = self.memory_usage_top_n_process + 6
      cmd = (
          f'top -o +%MEM -d {MEMORY_USAGE_DUMP_INTERVAL_SEC} -b | '
          f'grep "top -" -A {keep_first_n_lines}'
      )
      return _RemoteCommandOutputCollector(
          ssh, log_host_dir, command=cmd, excerpt_tag='top_memory_usage'
      )

    raise ConfigError(f'Got unknown log type: {log_type}')


class DeviceLogService(base_service.BaseService):
  """A service for streaming multiple CrOS device logs to host.

  Typical usage:

  .. code-block:: python

    from mobly.controllers.cros import cros_device

    crosd: cros_device.CrosDevice
    log_service_config = device_log_service.Config(
        log_types={
            device_log_service.LogType.CHROME_LOG,
            device_log_service.LogType.BLUETOOTH_MONITOR,
        })
    crosd.services.register('device_log_service',
                            device_log_service.DeviceLogService,
                            log_service_config)


  Attributes:
    log: A logger adapted from the CrOS device logger, which adds the identifier
      '[DeviceLogService]' to each log line: '<CrosDevice log prefix>
      [DeviceLogService] <message>'.
  """

  def __init__(self,
               device: 'CrosDevice',
               configs: Optional[Config] = None) -> None:
    """Initializes an instance.

    Args:
      device: The device controller object.
      configs: The configuration parameters for this service.
    """
    super().__init__(device, configs)
    self._device = device
    self._log = mobly_logger.PrefixLoggerAdapter(self._device.log, {
        mobly_logger.PrefixLoggerAdapter.EXTRA_KEY_LOG_PREFIX:
            '[DeviceLogService]'
    })
    self._configs = configs or Config()

    # Create a separate SSH session for log streaming so that it does not block
    # other SSH operations.
    self._ssh = ssh_lib.SSHProxy(
        self._device.hostname,
        self._device.ssh_port,
        username=constants.SSH_USERNAME,
        password=constants.SSH_PASSWORD)

    self._log_collectors = self._configs.create_log_collectors(
        self._ssh, pathlib.Path(self._device.log_path))

  def __del__(self) -> None:
    self._ssh.disconnect()

  @property
  def is_alive(self) -> bool:
    """True if the service is alive; False otherwise."""
    return any(map(lambda c: c.is_alive, self._log_collectors))

  def start(self) -> None:
    """Starts streaming the specified logs to host."""
    self._log.debug('Starting.')
    self._ssh.connect()
    for log_collector in self._log_collectors:
      log_collector.start_remote_process()

  def stop(self) -> None:
    """Stops streaming the specified logs to host."""
    self._log.debug('Stopping.')
    for log_collector in self._log_collectors:
      if not log_collector.is_alive:
        self._log.warning(
            'The process for streaming remote log "%s" has exited in advance, '
            'which might lead to log loss.', log_collector.excerpt_tag)
      log_collector.stop_remote_process()

    self._ssh.disconnect()

  def create_output_excerpts(
      self, test_info: runtime_test_info.RuntimeTestInfo) -> list[Any]:
    """Creates excerpts for specified logs and returns the excerpt paths."""
    self._log.debug('Creating output excerpts.')
    dest_path = test_info.output_path
    utils.create_dir(dest_path)
    timestamp = mobly_logger.get_log_file_timestamp()
    excerpts_paths = []

    for log_collector in self._log_collectors:
      filename = (f'cros_log,{log_collector.excerpt_tag},{self._device.serial},'
                  f'{self._device.build_info.board},{timestamp}.log')
      excerpts_path = pathlib.Path(dest_path, filename)
      log_collector.create_output_excerpts(excerpts_path)
      excerpts_paths.append(excerpts_path)
    return excerpts_paths

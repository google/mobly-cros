"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2023 The ChromiumOS Authors
Use of this source code is governed by a BSD-style license that can be
found in the LICENSE file.
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _BluetoothStackType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _BluetoothStackTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_BluetoothStackType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    BLUETOOTH_STACK_TYPE_NULL: _BluetoothStackType.ValueType  # 0
    BLUETOOTH_STACK_TYPE_BLUEZ: _BluetoothStackType.ValueType  # 1
    BLUETOOTH_STACK_TYPE_FLOSS: _BluetoothStackType.ValueType  # 2

class BluetoothStackType(_BluetoothStackType, metaclass=_BluetoothStackTypeEnumTypeWrapper): ...

BLUETOOTH_STACK_TYPE_NULL: BluetoothStackType.ValueType  # 0
BLUETOOTH_STACK_TYPE_BLUEZ: BluetoothStackType.ValueType  # 1
BLUETOOTH_STACK_TYPE_FLOSS: BluetoothStackType.ValueType  # 2
global___BluetoothStackType = BluetoothStackType

@typing.final
class BluetoothAdapterProperties(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POWERED_FIELD_NUMBER: builtins.int
    DISCOVERING_FIELD_NUMBER: builtins.int
    DISCOVERABLE_FIELD_NUMBER: builtins.int
    PAIRABLE_FIELD_NUMBER: builtins.int
    ADDRESS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    powered: builtins.bool
    """powered is true if the adapter is powered on."""
    discovering: builtins.bool
    """discovering is true if the adapter is in the discovering state."""
    discoverable: builtins.bool
    """discoverable is true if the adapter is discoverable externally."""
    pairable: builtins.bool
    """pairable is true if devices may be paired with the adapter."""
    address: builtins.str
    """address is the external bluetooth mac address of the adapter."""
    name: builtins.str
    """name is the external bluetooth name of the DUT."""
    def __init__(
        self,
        *,
        powered: builtins.bool = ...,
        discovering: builtins.bool = ...,
        discoverable: builtins.bool = ...,
        pairable: builtins.bool = ...,
        address: builtins.str = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["address", b"address", "discoverable", b"discoverable", "discovering", b"discovering", "name", b"name", "pairable", b"pairable", "powered", b"powered"]) -> None: ...

global___BluetoothAdapterProperties = BluetoothAdapterProperties

@typing.final
class BluetoothDeviceProperties(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    ALIAS_FIELD_NUMBER: builtins.int
    CONNECTED_FIELD_NUMBER: builtins.int
    PAIRED_FIELD_NUMBER: builtins.int
    address: builtins.str
    """address is the mac address of the bluetooth device."""
    name: builtins.str
    """name is the name of the bluetooth device."""
    alias: builtins.str
    """alias is the alias of the bluetooth device."""
    connected: builtins.bool
    """connected is true if the device is connected."""
    paired: builtins.bool
    """paired is true if the device is paired."""
    def __init__(
        self,
        *,
        address: builtins.str = ...,
        name: builtins.str = ...,
        alias: builtins.str = ...,
        connected: builtins.bool = ...,
        paired: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["address", b"address", "alias", b"alias", "connected", b"connected", "name", b"name", "paired", b"paired"]) -> None: ...

global___BluetoothDeviceProperties = BluetoothDeviceProperties

@typing.final
class SetBluetoothStackRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STACKTYPE_FIELD_NUMBER: builtins.int
    stackType: global___BluetoothStackType.ValueType
    def __init__(
        self,
        *,
        stackType: global___BluetoothStackType.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["stackType", b"stackType"]) -> None: ...

global___SetBluetoothStackRequest = SetBluetoothStackRequest

@typing.final
class StackTypeResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STACKTYPE_FIELD_NUMBER: builtins.int
    stackType: global___BluetoothStackType.ValueType
    def __init__(
        self,
        *,
        stackType: global___BluetoothStackType.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["stackType", b"stackType"]) -> None: ...

global___StackTypeResponse = StackTypeResponse

@typing.final
class ResetRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POWERON_FIELD_NUMBER: builtins.int
    powerOn: builtins.bool
    def __init__(
        self,
        *,
        powerOn: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["powerOn", b"powerOn"]) -> None: ...

global___ResetRequest = ResetRequest

@typing.final
class AdapterPropertiesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADAPTERPROPERTIES_FIELD_NUMBER: builtins.int
    @property
    def adapterProperties(self) -> global___BluetoothAdapterProperties: ...
    def __init__(
        self,
        *,
        adapterProperties: global___BluetoothAdapterProperties | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["adapterProperties", b"adapterProperties"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["adapterProperties", b"adapterProperties"]) -> None: ...

global___AdapterPropertiesResponse = AdapterPropertiesResponse

@typing.final
class IsPoweredOnResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ISPOWEREDON_FIELD_NUMBER: builtins.int
    isPoweredOn: builtins.bool
    def __init__(
        self,
        *,
        isPoweredOn: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["isPoweredOn", b"isPoweredOn"]) -> None: ...

global___IsPoweredOnResponse = IsPoweredOnResponse

@typing.final
class SetPoweredRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POWERED_FIELD_NUMBER: builtins.int
    powered: builtins.bool
    def __init__(
        self,
        *,
        powered: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["powered", b"powered"]) -> None: ...

global___SetPoweredRequest = SetPoweredRequest

@typing.final
class SetLLPrivacyRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENABLED_FIELD_NUMBER: builtins.int
    enabled: builtins.bool
    def __init__(
        self,
        *,
        enabled: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["enabled", b"enabled"]) -> None: ...

global___SetLLPrivacyRequest = SetLLPrivacyRequest

@typing.final
class IsDiscoveringResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ISDISCOVERING_FIELD_NUMBER: builtins.int
    isDiscovering: builtins.bool
    def __init__(
        self,
        *,
        isDiscovering: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["isDiscovering", b"isDiscovering"]) -> None: ...

global___IsDiscoveringResponse = IsDiscoveringResponse

@typing.final
class IsDiscoverableResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ISDISCOVERABLE_FIELD_NUMBER: builtins.int
    isDiscoverable: builtins.bool
    def __init__(
        self,
        *,
        isDiscoverable: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["isDiscoverable", b"isDiscoverable"]) -> None: ...

global___IsDiscoverableResponse = IsDiscoverableResponse

@typing.final
class SetDiscoverableRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DISCOVERABLE_FIELD_NUMBER: builtins.int
    discoverable: builtins.bool
    def __init__(
        self,
        *,
        discoverable: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["discoverable", b"discoverable"]) -> None: ...

global___SetDiscoverableRequest = SetDiscoverableRequest

@typing.final
class SetDiscoverableWithTimeoutRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DISCOVERABLE_FIELD_NUMBER: builtins.int
    TIMEOUTSECONDS_FIELD_NUMBER: builtins.int
    discoverable: builtins.bool
    timeoutSeconds: builtins.int
    def __init__(
        self,
        *,
        discoverable: builtins.bool = ...,
        timeoutSeconds: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["discoverable", b"discoverable", "timeoutSeconds", b"timeoutSeconds"]) -> None: ...

global___SetDiscoverableWithTimeoutRequest = SetDiscoverableWithTimeoutRequest

@typing.final
class IsPairableResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ISPAIRABLE_FIELD_NUMBER: builtins.int
    isPairable: builtins.bool
    def __init__(
        self,
        *,
        isPairable: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["isPairable", b"isPairable"]) -> None: ...

global___IsPairableResponse = IsPairableResponse

@typing.final
class SetPairableRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PAIRABLE_FIELD_NUMBER: builtins.int
    pairable: builtins.bool
    def __init__(
        self,
        *,
        pairable: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["pairable", b"pairable"]) -> None: ...

global___SetPairableRequest = SetPairableRequest

@typing.final
class AddressResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADAPTERADDRESS_FIELD_NUMBER: builtins.int
    adapterAddress: builtins.str
    def __init__(
        self,
        *,
        adapterAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["adapterAddress", b"adapterAddress"]) -> None: ...

global___AddressResponse = AddressResponse

@typing.final
class NameResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADAPTERNAME_FIELD_NUMBER: builtins.int
    adapterName: builtins.str
    def __init__(
        self,
        *,
        adapterName: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["adapterName", b"adapterName"]) -> None: ...

global___NameResponse = NameResponse

@typing.final
class UUIDsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADAPTERUUIDS_FIELD_NUMBER: builtins.int
    @property
    def adapterUUIDs(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        adapterUUIDs: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["adapterUUIDs", b"adapterUUIDs"]) -> None: ...

global___UUIDsResponse = UUIDsResponse

@typing.final
class DevicesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KNOWNDEVICEADDRESSES_FIELD_NUMBER: builtins.int
    @property
    def knownDeviceAddresses(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        knownDeviceAddresses: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["knownDeviceAddresses", b"knownDeviceAddresses"]) -> None: ...

global___DevicesResponse = DevicesResponse

@typing.final
class HasDeviceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___HasDeviceRequest = HasDeviceRequest

@typing.final
class HasDeviceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HASDEVICE_FIELD_NUMBER: builtins.int
    hasDevice: builtins.bool
    def __init__(
        self,
        *,
        hasDevice: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["hasDevice", b"hasDevice"]) -> None: ...

global___HasDeviceResponse = HasDeviceResponse

@typing.final
class RemoveDeviceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___RemoveDeviceRequest = RemoveDeviceRequest

@typing.final
class ConnectDeviceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___ConnectDeviceRequest = ConnectDeviceRequest

@typing.final
class DisconnectDeviceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___DisconnectDeviceRequest = DisconnectDeviceRequest

@typing.final
class WaitForConnectStateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    EXPECTEDCONNECTSTATE_FIELD_NUMBER: builtins.int
    TIMEOUT_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    expectedConnectState: builtins.bool
    @property
    def timeout(self) -> google.protobuf.duration_pb2.Duration: ...
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
        expectedConnectState: builtins.bool = ...,
        timeout: google.protobuf.duration_pb2.Duration | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["_timeout", b"_timeout", "timeout", b"timeout"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["_timeout", b"_timeout", "deviceAddress", b"deviceAddress", "expectedConnectState", b"expectedConnectState", "timeout", b"timeout"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["_timeout", b"_timeout"]) -> typing.Literal["timeout"] | None: ...

global___WaitForConnectStateRequest = WaitForConnectStateRequest

@typing.final
class DevicePropertiesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___DevicePropertiesRequest = DevicePropertiesRequest

@typing.final
class DevicePropertiesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEPROPERTIES_FIELD_NUMBER: builtins.int
    @property
    def deviceProperties(self) -> global___BluetoothDeviceProperties: ...
    def __init__(
        self,
        *,
        deviceProperties: global___BluetoothDeviceProperties | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["deviceProperties", b"deviceProperties"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["deviceProperties", b"deviceProperties"]) -> None: ...

global___DevicePropertiesResponse = DevicePropertiesResponse

@typing.final
class DeviceIsConnectedRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___DeviceIsConnectedRequest = DeviceIsConnectedRequest

@typing.final
class DeviceIsConnectedResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEISCONNECTED_FIELD_NUMBER: builtins.int
    deviceIsConnected: builtins.bool
    def __init__(
        self,
        *,
        deviceIsConnected: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceIsConnected", b"deviceIsConnected"]) -> None: ...

global___DeviceIsConnectedResponse = DeviceIsConnectedResponse

@typing.final
class DeviceIsPairedRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___DeviceIsPairedRequest = DeviceIsPairedRequest

@typing.final
class DeviceIsPairedResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEISPAIRED_FIELD_NUMBER: builtins.int
    deviceIsPaired: builtins.bool
    def __init__(
        self,
        *,
        deviceIsPaired: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceIsPaired", b"deviceIsPaired"]) -> None: ...

global___DeviceIsPairedResponse = DeviceIsPairedResponse

@typing.final
class DeviceAddressRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICENAME_FIELD_NUMBER: builtins.int
    deviceName: builtins.str
    def __init__(
        self,
        *,
        deviceName: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceName", b"deviceName"]) -> None: ...

global___DeviceAddressRequest = DeviceAddressRequest

@typing.final
class DeviceAddressResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___DeviceAddressResponse = DeviceAddressResponse

@typing.final
class DeviceNameRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___DeviceNameRequest = DeviceNameRequest

@typing.final
class DeviceNameResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICENAME_FIELD_NUMBER: builtins.int
    deviceName: builtins.str
    def __init__(
        self,
        *,
        deviceName: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceName", b"deviceName"]) -> None: ...

global___DeviceNameResponse = DeviceNameResponse

@typing.final
class DeviceAliasRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___DeviceAliasRequest = DeviceAliasRequest

@typing.final
class DeviceAliasResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEALIAS_FIELD_NUMBER: builtins.int
    deviceAlias: builtins.str
    def __init__(
        self,
        *,
        deviceAlias: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAlias", b"deviceAlias"]) -> None: ...

global___DeviceAliasResponse = DeviceAliasResponse

@typing.final
class DiscoverDeviceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    DISCOVERYTIMEOUT_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    @property
    def discoveryTimeout(self) -> google.protobuf.duration_pb2.Duration: ...
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
        discoveryTimeout: google.protobuf.duration_pb2.Duration | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["discoveryTimeout", b"discoveryTimeout"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress", "discoveryTimeout", b"discoveryTimeout"]) -> None: ...

global___DiscoverDeviceRequest = DiscoverDeviceRequest

@typing.final
class PairDeviceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    PIN_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    pin: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
        pin: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress", "pin", b"pin"]) -> None: ...

global___PairDeviceRequest = PairDeviceRequest

@typing.final
class EnabledOnBootResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADAPTER_ENABLED_ON_BOOT_FIELD_NUMBER: builtins.int
    adapter_enabled_on_boot: builtins.bool
    def __init__(
        self,
        *,
        adapter_enabled_on_boot: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["adapter_enabled_on_boot", b"adapter_enabled_on_boot"]) -> None: ...

global___EnabledOnBootResponse = EnabledOnBootResponse

@typing.final
class SetEnabledOnBootRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADAPTER_ENABLED_ON_BOOT_FIELD_NUMBER: builtins.int
    adapter_enabled_on_boot: builtins.bool
    def __init__(
        self,
        *,
        adapter_enabled_on_boot: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["adapter_enabled_on_boot", b"adapter_enabled_on_boot"]) -> None: ...

global___SetEnabledOnBootRequest = SetEnabledOnBootRequest

@typing.final
class SetDebugLogLevelsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LEVEL_FIELD_NUMBER: builtins.int
    level: builtins.int
    def __init__(
        self,
        *,
        level: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["level", b"level"]) -> None: ...

global___SetDebugLogLevelsRequest = SetDebugLogLevelsRequest

@typing.final
class IsWBSSupportedResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    WBS_SUPPORTED_FIELD_NUMBER: builtins.int
    wbs_supported: builtins.bool
    def __init__(
        self,
        *,
        wbs_supported: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["wbs_supported", b"wbs_supported"]) -> None: ...

global___IsWBSSupportedResponse = IsWBSSupportedResponse

@typing.final
class IsSWBSupportedResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SWB_SUPPORTED_FIELD_NUMBER: builtins.int
    swb_supported: builtins.bool
    def __init__(
        self,
        *,
        swb_supported: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["swb_supported", b"swb_supported"]) -> None: ...

global___IsSWBSupportedResponse = IsSWBSupportedResponse

@typing.final
class GetPasskeyRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEVICEADDRESS_FIELD_NUMBER: builtins.int
    deviceAddress: builtins.str
    def __init__(
        self,
        *,
        deviceAddress: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["deviceAddress", b"deviceAddress"]) -> None: ...

global___GetPasskeyRequest = GetPasskeyRequest

@typing.final
class GetPasskeyResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PASSKEY_FIELD_NUMBER: builtins.int
    passkey: builtins.int
    def __init__(
        self,
        *,
        passkey: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["passkey", b"passkey"]) -> None: ...

global___GetPasskeyResponse = GetPasskeyResponse

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tast/cros/services/cros/bluetooth/bluetooth_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'tast/cros/services/cros/bluetooth/bluetooth_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9tast/cros/services/cros/bluetooth/bluetooth_service.proto\x12\x13tast.cros.bluetooth\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1egoogle/protobuf/duration.proto\"\x89\x01\n\x1a\x42luetoothAdapterProperties\x12\x0f\n\x07powered\x18\x01 \x01(\x08\x12\x13\n\x0b\x64iscovering\x18\x02 \x01(\x08\x12\x14\n\x0c\x64iscoverable\x18\x03 \x01(\x08\x12\x10\n\x08pairable\x18\x04 \x01(\x08\x12\x0f\n\x07\x61\x64\x64ress\x18\x05 \x01(\t\x12\x0c\n\x04name\x18\x06 \x01(\t\"l\n\x19\x42luetoothDeviceProperties\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05\x61lias\x18\x03 \x01(\t\x12\x11\n\tconnected\x18\x04 \x01(\x08\x12\x0e\n\x06paired\x18\x05 \x01(\x08\"V\n\x18SetBluetoothStackRequest\x12:\n\tstackType\x18\x01 \x01(\x0e\x32\'.tast.cros.bluetooth.BluetoothStackType\"O\n\x11StackTypeResponse\x12:\n\tstackType\x18\x01 \x01(\x0e\x32\'.tast.cros.bluetooth.BluetoothStackType\"\x1f\n\x0cResetRequest\x12\x0f\n\x07powerOn\x18\x01 \x01(\x08\"g\n\x19\x41\x64\x61pterPropertiesResponse\x12J\n\x11\x61\x64\x61pterProperties\x18\x01 \x01(\x0b\x32/.tast.cros.bluetooth.BluetoothAdapterProperties\"*\n\x13IsPoweredOnResponse\x12\x13\n\x0bisPoweredOn\x18\x01 \x01(\x08\"$\n\x11SetPoweredRequest\x12\x0f\n\x07powered\x18\x01 \x01(\x08\"&\n\x13SetLLPrivacyRequest\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\".\n\x15IsDiscoveringResponse\x12\x15\n\risDiscovering\x18\x01 \x01(\x08\"0\n\x16IsDiscoverableResponse\x12\x16\n\x0eisDiscoverable\x18\x01 \x01(\x08\".\n\x16SetDiscoverableRequest\x12\x14\n\x0c\x64iscoverable\x18\x01 \x01(\x08\"Q\n!SetDiscoverableWithTimeoutRequest\x12\x14\n\x0c\x64iscoverable\x18\x01 \x01(\x08\x12\x16\n\x0etimeoutSeconds\x18\x02 \x01(\r\"(\n\x12IsPairableResponse\x12\x12\n\nisPairable\x18\x01 \x01(\x08\"&\n\x12SetPairableRequest\x12\x10\n\x08pairable\x18\x01 \x01(\x08\")\n\x0f\x41\x64\x64ressResponse\x12\x16\n\x0e\x61\x64\x61pterAddress\x18\x01 \x01(\t\"#\n\x0cNameResponse\x12\x13\n\x0b\x61\x64\x61pterName\x18\x01 \x01(\t\"%\n\rUUIDsResponse\x12\x14\n\x0c\x61\x64\x61pterUUIDs\x18\x01 \x03(\t\"/\n\x0f\x44\x65vicesResponse\x12\x1c\n\x14knownDeviceAddresses\x18\x01 \x03(\t\")\n\x10HasDeviceRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"&\n\x11HasDeviceResponse\x12\x11\n\thasDevice\x18\x01 \x01(\x08\",\n\x13RemoveDeviceRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"-\n\x14\x43onnectDeviceRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"0\n\x17\x44isconnectDeviceRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"\x8e\x01\n\x1aWaitForConnectStateRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\x12\x1c\n\x14\x65xpectedConnectState\x18\x02 \x01(\x08\x12/\n\x07timeout\x18\x03 \x01(\x0b\x32\x19.google.protobuf.DurationH\x00\x88\x01\x01\x42\n\n\x08_timeout\"0\n\x17\x44\x65vicePropertiesRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"d\n\x18\x44\x65vicePropertiesResponse\x12H\n\x10\x64\x65viceProperties\x18\x01 \x01(\x0b\x32..tast.cros.bluetooth.BluetoothDeviceProperties\"1\n\x18\x44\x65viceIsConnectedRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"6\n\x19\x44\x65viceIsConnectedResponse\x12\x19\n\x11\x64\x65viceIsConnected\x18\x01 \x01(\x08\".\n\x15\x44\x65viceIsPairedRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"0\n\x16\x44\x65viceIsPairedResponse\x12\x16\n\x0e\x64\x65viceIsPaired\x18\x01 \x01(\x08\"*\n\x14\x44\x65viceAddressRequest\x12\x12\n\ndeviceName\x18\x01 \x01(\t\".\n\x15\x44\x65viceAddressResponse\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"*\n\x11\x44\x65viceNameRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"(\n\x12\x44\x65viceNameResponse\x12\x12\n\ndeviceName\x18\x01 \x01(\t\"+\n\x12\x44\x65viceAliasRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"*\n\x13\x44\x65viceAliasResponse\x12\x13\n\x0b\x64\x65viceAlias\x18\x01 \x01(\t\"i\n\x15\x44iscoverDeviceRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\x12\x33\n\x10\x64iscoveryTimeout\x18\x03 \x01(\x0b\x32\x19.google.protobuf.DurationJ\x04\x08\x02\x10\x03\"7\n\x11PairDeviceRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\x12\x0b\n\x03pin\x18\x02 \x01(\t\"8\n\x15\x45nabledOnBootResponse\x12\x1f\n\x17\x61\x64\x61pter_enabled_on_boot\x18\x01 \x01(\x08\":\n\x17SetEnabledOnBootRequest\x12\x1f\n\x17\x61\x64\x61pter_enabled_on_boot\x18\x01 \x01(\x08\")\n\x18SetDebugLogLevelsRequest\x12\r\n\x05level\x18\x01 \x01(\r\"/\n\x16IsWBSSupportedResponse\x12\x15\n\rwbs_supported\x18\x01 \x01(\x08\"/\n\x16IsSWBSupportedResponse\x12\x15\n\rswb_supported\x18\x01 \x01(\x08\"*\n\x11GetPasskeyRequest\x12\x15\n\rdeviceAddress\x18\x01 \x01(\t\"%\n\x12GetPasskeyResponse\x12\x0f\n\x07passkey\x18\x01 \x01(\r*s\n\x12\x42luetoothStackType\x12\x1d\n\x19\x42LUETOOTH_STACK_TYPE_NULL\x10\x00\x12\x1e\n\x1a\x42LUETOOTH_STACK_TYPE_BLUEZ\x10\x01\x12\x1e\n\x1a\x42LUETOOTH_STACK_TYPE_FLOSS\x10\x02\x32\x82\x1b\n\x10\x42luetoothService\x12H\n\x14SetupBluetoothFacade\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\\\n\x11SetBluetoothStack\x12-.tast.cros.bluetooth.SetBluetoothStackRequest\x1a\x16.google.protobuf.Empty\"\x00\x12M\n\tStackType\x12\x16.google.protobuf.Empty\x1a&.tast.cros.bluetooth.StackTypeResponse\"\x00\x12\x44\n\x05Reset\x12!.tast.cros.bluetooth.ResetRequest\x1a\x16.google.protobuf.Empty\"\x00\x12]\n\x11\x41\x64\x61pterProperties\x12\x16.google.protobuf.Empty\x1a..tast.cros.bluetooth.AdapterPropertiesResponse\"\x00\x12Q\n\x0bIsPoweredOn\x12\x16.google.protobuf.Empty\x1a(.tast.cros.bluetooth.IsPoweredOnResponse\"\x00\x12N\n\nSetPowered\x12&.tast.cros.bluetooth.SetPoweredRequest\x1a\x16.google.protobuf.Empty\"\x00\x12R\n\x0cSetLLPrivacy\x12(.tast.cros.bluetooth.SetLLPrivacyRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x42\n\x0eStartDiscovery\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\x41\n\rStopDiscovery\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12U\n\rIsDiscovering\x12\x16.google.protobuf.Empty\x1a*.tast.cros.bluetooth.IsDiscoveringResponse\"\x00\x12W\n\x0eIsDiscoverable\x12\x16.google.protobuf.Empty\x1a+.tast.cros.bluetooth.IsDiscoverableResponse\"\x00\x12X\n\x0fSetDiscoverable\x12+.tast.cros.bluetooth.SetDiscoverableRequest\x1a\x16.google.protobuf.Empty\"\x00\x12n\n\x1aSetDiscoverableWithTimeout\x12\x36.tast.cros.bluetooth.SetDiscoverableWithTimeoutRequest\x1a\x16.google.protobuf.Empty\"\x00\x12O\n\nIsPairable\x12\x16.google.protobuf.Empty\x1a\'.tast.cros.bluetooth.IsPairableResponse\"\x00\x12P\n\x0bSetPairable\x12\'.tast.cros.bluetooth.SetPairableRequest\x1a\x16.google.protobuf.Empty\"\x00\x12I\n\x07\x41\x64\x64ress\x12\x16.google.protobuf.Empty\x1a$.tast.cros.bluetooth.AddressResponse\"\x00\x12\x43\n\x04Name\x12\x16.google.protobuf.Empty\x1a!.tast.cros.bluetooth.NameResponse\"\x00\x12\x45\n\x05UUIDs\x12\x16.google.protobuf.Empty\x1a\".tast.cros.bluetooth.UUIDsResponse\"\x00\x12I\n\x07\x44\x65vices\x12\x16.google.protobuf.Empty\x1a$.tast.cros.bluetooth.DevicesResponse\"\x00\x12\\\n\tHasDevice\x12%.tast.cros.bluetooth.HasDeviceRequest\x1a&.tast.cros.bluetooth.HasDeviceResponse\"\x00\x12R\n\x0cRemoveDevice\x12(.tast.cros.bluetooth.RemoveDeviceRequest\x1a\x16.google.protobuf.Empty\"\x00\x12T\n\rConnectDevice\x12).tast.cros.bluetooth.ConnectDeviceRequest\x1a\x16.google.protobuf.Empty\"\x00\x12Z\n\x10\x44isconnectDevice\x12,.tast.cros.bluetooth.DisconnectDeviceRequest\x1a\x16.google.protobuf.Empty\"\x00\x12`\n\x13WaitForConnectState\x12/.tast.cros.bluetooth.WaitForConnectStateRequest\x1a\x16.google.protobuf.Empty\"\x00\x12q\n\x10\x44\x65viceProperties\x12,.tast.cros.bluetooth.DevicePropertiesRequest\x1a-.tast.cros.bluetooth.DevicePropertiesResponse\"\x00\x12t\n\x11\x44\x65viceIsConnected\x12-.tast.cros.bluetooth.DeviceIsConnectedRequest\x1a..tast.cros.bluetooth.DeviceIsConnectedResponse\"\x00\x12k\n\x0e\x44\x65viceIsPaired\x12*.tast.cros.bluetooth.DeviceIsPairedRequest\x1a+.tast.cros.bluetooth.DeviceIsPairedResponse\"\x00\x12h\n\rDeviceAddress\x12).tast.cros.bluetooth.DeviceAddressRequest\x1a*.tast.cros.bluetooth.DeviceAddressResponse\"\x00\x12_\n\nDeviceName\x12&.tast.cros.bluetooth.DeviceNameRequest\x1a\'.tast.cros.bluetooth.DeviceNameResponse\"\x00\x12\x62\n\x0b\x44\x65viceAlias\x12\'.tast.cros.bluetooth.DeviceAliasRequest\x1a(.tast.cros.bluetooth.DeviceAliasResponse\"\x00\x12V\n\x0e\x44iscoverDevice\x12*.tast.cros.bluetooth.DiscoverDeviceRequest\x1a\x16.google.protobuf.Empty\"\x00\x12N\n\nPairDevice\x12&.tast.cros.bluetooth.PairDeviceRequest\x1a\x16.google.protobuf.Empty\"\x00\x12U\n\rEnabledOnBoot\x12\x16.google.protobuf.Empty\x1a*.tast.cros.bluetooth.EnabledOnBootResponse\"\x00\x12Z\n\x10SetEnabledOnBoot\x12,.tast.cros.bluetooth.SetEnabledOnBootRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\\\n\x11SetDebugLogLevels\x12-.tast.cros.bluetooth.SetDebugLogLevelsRequest\x1a\x16.google.protobuf.Empty\"\x00\x12W\n\x0eIsWBSSupported\x12\x16.google.protobuf.Empty\x1a+.tast.cros.bluetooth.IsWBSSupportedResponse\"\x00\x12W\n\x0eIsSWBSupported\x12\x16.google.protobuf.Empty\x1a+.tast.cros.bluetooth.IsSWBSupportedResponse\"\x00\x12_\n\nGetPasskey\x12&.tast.cros.bluetooth.GetPasskeyRequest\x1a\'.tast.cros.bluetooth.GetPasskeyResponse\"\x00\x42\x39Z7go.chromium.org/tast-tests/cros/services/cros/bluetoothb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tast.cros.services.cros.bluetooth.bluetooth_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7go.chromium.org/tast-tests/cros/services/cros/bluetooth'
  _globals['_BLUETOOTHSTACKTYPE']._serialized_start=2802
  _globals['_BLUETOOTHSTACKTYPE']._serialized_end=2917
  _globals['_BLUETOOTHADAPTERPROPERTIES']._serialized_start=144
  _globals['_BLUETOOTHADAPTERPROPERTIES']._serialized_end=281
  _globals['_BLUETOOTHDEVICEPROPERTIES']._serialized_start=283
  _globals['_BLUETOOTHDEVICEPROPERTIES']._serialized_end=391
  _globals['_SETBLUETOOTHSTACKREQUEST']._serialized_start=393
  _globals['_SETBLUETOOTHSTACKREQUEST']._serialized_end=479
  _globals['_STACKTYPERESPONSE']._serialized_start=481
  _globals['_STACKTYPERESPONSE']._serialized_end=560
  _globals['_RESETREQUEST']._serialized_start=562
  _globals['_RESETREQUEST']._serialized_end=593
  _globals['_ADAPTERPROPERTIESRESPONSE']._serialized_start=595
  _globals['_ADAPTERPROPERTIESRESPONSE']._serialized_end=698
  _globals['_ISPOWEREDONRESPONSE']._serialized_start=700
  _globals['_ISPOWEREDONRESPONSE']._serialized_end=742
  _globals['_SETPOWEREDREQUEST']._serialized_start=744
  _globals['_SETPOWEREDREQUEST']._serialized_end=780
  _globals['_SETLLPRIVACYREQUEST']._serialized_start=782
  _globals['_SETLLPRIVACYREQUEST']._serialized_end=820
  _globals['_ISDISCOVERINGRESPONSE']._serialized_start=822
  _globals['_ISDISCOVERINGRESPONSE']._serialized_end=868
  _globals['_ISDISCOVERABLERESPONSE']._serialized_start=870
  _globals['_ISDISCOVERABLERESPONSE']._serialized_end=918
  _globals['_SETDISCOVERABLEREQUEST']._serialized_start=920
  _globals['_SETDISCOVERABLEREQUEST']._serialized_end=966
  _globals['_SETDISCOVERABLEWITHTIMEOUTREQUEST']._serialized_start=968
  _globals['_SETDISCOVERABLEWITHTIMEOUTREQUEST']._serialized_end=1049
  _globals['_ISPAIRABLERESPONSE']._serialized_start=1051
  _globals['_ISPAIRABLERESPONSE']._serialized_end=1091
  _globals['_SETPAIRABLEREQUEST']._serialized_start=1093
  _globals['_SETPAIRABLEREQUEST']._serialized_end=1131
  _globals['_ADDRESSRESPONSE']._serialized_start=1133
  _globals['_ADDRESSRESPONSE']._serialized_end=1174
  _globals['_NAMERESPONSE']._serialized_start=1176
  _globals['_NAMERESPONSE']._serialized_end=1211
  _globals['_UUIDSRESPONSE']._serialized_start=1213
  _globals['_UUIDSRESPONSE']._serialized_end=1250
  _globals['_DEVICESRESPONSE']._serialized_start=1252
  _globals['_DEVICESRESPONSE']._serialized_end=1299
  _globals['_HASDEVICEREQUEST']._serialized_start=1301
  _globals['_HASDEVICEREQUEST']._serialized_end=1342
  _globals['_HASDEVICERESPONSE']._serialized_start=1344
  _globals['_HASDEVICERESPONSE']._serialized_end=1382
  _globals['_REMOVEDEVICEREQUEST']._serialized_start=1384
  _globals['_REMOVEDEVICEREQUEST']._serialized_end=1428
  _globals['_CONNECTDEVICEREQUEST']._serialized_start=1430
  _globals['_CONNECTDEVICEREQUEST']._serialized_end=1475
  _globals['_DISCONNECTDEVICEREQUEST']._serialized_start=1477
  _globals['_DISCONNECTDEVICEREQUEST']._serialized_end=1525
  _globals['_WAITFORCONNECTSTATEREQUEST']._serialized_start=1528
  _globals['_WAITFORCONNECTSTATEREQUEST']._serialized_end=1670
  _globals['_DEVICEPROPERTIESREQUEST']._serialized_start=1672
  _globals['_DEVICEPROPERTIESREQUEST']._serialized_end=1720
  _globals['_DEVICEPROPERTIESRESPONSE']._serialized_start=1722
  _globals['_DEVICEPROPERTIESRESPONSE']._serialized_end=1822
  _globals['_DEVICEISCONNECTEDREQUEST']._serialized_start=1824
  _globals['_DEVICEISCONNECTEDREQUEST']._serialized_end=1873
  _globals['_DEVICEISCONNECTEDRESPONSE']._serialized_start=1875
  _globals['_DEVICEISCONNECTEDRESPONSE']._serialized_end=1929
  _globals['_DEVICEISPAIREDREQUEST']._serialized_start=1931
  _globals['_DEVICEISPAIREDREQUEST']._serialized_end=1977
  _globals['_DEVICEISPAIREDRESPONSE']._serialized_start=1979
  _globals['_DEVICEISPAIREDRESPONSE']._serialized_end=2027
  _globals['_DEVICEADDRESSREQUEST']._serialized_start=2029
  _globals['_DEVICEADDRESSREQUEST']._serialized_end=2071
  _globals['_DEVICEADDRESSRESPONSE']._serialized_start=2073
  _globals['_DEVICEADDRESSRESPONSE']._serialized_end=2119
  _globals['_DEVICENAMEREQUEST']._serialized_start=2121
  _globals['_DEVICENAMEREQUEST']._serialized_end=2163
  _globals['_DEVICENAMERESPONSE']._serialized_start=2165
  _globals['_DEVICENAMERESPONSE']._serialized_end=2205
  _globals['_DEVICEALIASREQUEST']._serialized_start=2207
  _globals['_DEVICEALIASREQUEST']._serialized_end=2250
  _globals['_DEVICEALIASRESPONSE']._serialized_start=2252
  _globals['_DEVICEALIASRESPONSE']._serialized_end=2294
  _globals['_DISCOVERDEVICEREQUEST']._serialized_start=2296
  _globals['_DISCOVERDEVICEREQUEST']._serialized_end=2401
  _globals['_PAIRDEVICEREQUEST']._serialized_start=2403
  _globals['_PAIRDEVICEREQUEST']._serialized_end=2458
  _globals['_ENABLEDONBOOTRESPONSE']._serialized_start=2460
  _globals['_ENABLEDONBOOTRESPONSE']._serialized_end=2516
  _globals['_SETENABLEDONBOOTREQUEST']._serialized_start=2518
  _globals['_SETENABLEDONBOOTREQUEST']._serialized_end=2576
  _globals['_SETDEBUGLOGLEVELSREQUEST']._serialized_start=2578
  _globals['_SETDEBUGLOGLEVELSREQUEST']._serialized_end=2619
  _globals['_ISWBSSUPPORTEDRESPONSE']._serialized_start=2621
  _globals['_ISWBSSUPPORTEDRESPONSE']._serialized_end=2668
  _globals['_ISSWBSUPPORTEDRESPONSE']._serialized_start=2670
  _globals['_ISSWBSUPPORTEDRESPONSE']._serialized_end=2717
  _globals['_GETPASSKEYREQUEST']._serialized_start=2719
  _globals['_GETPASSKEYREQUEST']._serialized_end=2761
  _globals['_GETPASSKEYRESPONSE']._serialized_start=2763
  _globals['_GETPASSKEYRESPONSE']._serialized_end=2800
  _globals['_BLUETOOTHSERVICE']._serialized_start=2920
  _globals['_BLUETOOTHSERVICE']._serialized_end=6378
# @@protoc_insertion_point(module_scope)

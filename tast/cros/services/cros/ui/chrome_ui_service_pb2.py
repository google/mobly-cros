# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tast/cros/services/cros/ui/chrome_ui_service.proto
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
    'tast/cros/services/cros/ui/chrome_ui_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2tast/cros/services/cros/ui/chrome_ui_service.proto\x12\x0ctast.cros.ui\x1a\x1bgoogle/protobuf/empty.proto\"<\n%DumpUITreeWithScreenshotToFileRequest\x12\x13\n\x0b\x66ile_prefix\x18\x01 \x01(\t2\xd3\x02\n\x0f\x43hromeUIService\x12\x45\n\x11\x45nsureLoginScreen\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12>\n\nDumpUITree\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12o\n\x1e\x44umpUITreeWithScreenshotToFile\x12\x33.tast.cros.ui.DumpUITreeWithScreenshotToFileRequest\x1a\x16.google.protobuf.Empty\"\x00\x12H\n\x14WaitForWelcomeScreen\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x42\x32Z0go.chromium.org/tast-tests/cros/services/cros/uib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tast.cros.services.cros.ui.chrome_ui_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z0go.chromium.org/tast-tests/cros/services/cros/ui'
  _globals['_DUMPUITREEWITHSCREENSHOTTOFILEREQUEST']._serialized_start=97
  _globals['_DUMPUITREEWITHSCREENSHOTTOFILEREQUEST']._serialized_end=157
  _globals['_CHROMEUISERVICE']._serialized_start=160
  _globals['_CHROMEUISERVICE']._serialized_end=499
# @@protoc_insertion_point(module_scope)

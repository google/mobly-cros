# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tast/cros/services/cros/ui/tconn_service.proto
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
    'tast/cros/services/cros/ui/tconn_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.tast/cros/services/cros/ui/tconn_service.proto\x12\x0ctast.cros.ui\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\"!\n\x0b\x45valRequest\x12\x0c\n\x04\x65xpr\x18\x01 \x01(\tJ\x04\x08\x02\x10\x03\"E\n\x0b\x43\x61llRequest\x12\n\n\x02\x66n\x18\x01 \x01(\t\x12$\n\x04\x61rgs\x18\x02 \x03(\x0b\x32\x16.google.protobuf.ValueJ\x04\x08\x03\x10\x04\"S\n\x12WaitForExprRequest\x12\x0c\n\x04\x65xpr\x18\x01 \x01(\t\x12\x14\n\x0ctimeout_secs\x18\x02 \x01(\r\x12\x13\n\x0b\x66\x61il_on_err\x18\x03 \x01(\x08J\x04\x08\x04\x10\x05\x32\x98\x02\n\x0cTconnService\x12;\n\x04\x45val\x12\x19.tast.cros.ui.EvalRequest\x1a\x16.google.protobuf.Value\"\x00\x12;\n\x04\x43\x61ll\x12\x19.tast.cros.ui.CallRequest\x1a\x16.google.protobuf.Value\"\x00\x12I\n\x0bWaitForExpr\x12 .tast.cros.ui.WaitForExprRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x43\n\x0fResetAutomation\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x42\x32Z0go.chromium.org/tast-tests/cros/services/cros/uib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tast.cros.services.cros.ui.tconn_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z0go.chromium.org/tast-tests/cros/services/cros/ui'
  _globals['_EVALREQUEST']._serialized_start=123
  _globals['_EVALREQUEST']._serialized_end=156
  _globals['_CALLREQUEST']._serialized_start=158
  _globals['_CALLREQUEST']._serialized_end=227
  _globals['_WAITFOREXPRREQUEST']._serialized_start=229
  _globals['_WAITFOREXPRREQUEST']._serialized_end=312
  _globals['_TCONNSERVICE']._serialized_start=315
  _globals['_TCONNSERVICE']._serialized_end=595
# @@protoc_insertion_point(module_scope)

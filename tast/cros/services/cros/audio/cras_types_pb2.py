# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tast/cros/services/cros/audio/cras_types.proto
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
    'tast/cros/services/cros/audio/cras_types.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.tast/cros/services/cros/audio/cras_types.proto\x12\x0ftast.cros.audio\"4\n\nCrasNodeID\x12\x13\n\x0b\x64\x65viceIndex\x18\x01 \x01(\x05\x12\x11\n\tnodeIndex\x18\x02 \x01(\x05\"\x8f\x01\n\x08\x43rasNode\x12\x10\n\x08is_input\x18\x01 \x01(\x08\x12\n\n\x02id\x18\x02 \x01(\x04\x12+\n\x04type\x18\x03 \x01(\x0e\x32\x1d.tast.cros.audio.CrasNodeType\x12\x13\n\x0b\x64\x65vice_name\x18\x04 \x01(\t\x12\x0e\n\x06\x61\x63tive\x18\x05 \x01(\x08\x12\x13\n\x0bnode_volume\x18\x06 \x01(\x04*\xa7\x06\n\x0c\x43rasNodeType\x12\x1a\n\x16\x43RAS_NODE_TYPE_UNKNOWN\x10\x00\x12#\n\x1f\x43RAS_NODE_TYPE_INTERNAL_SPEAKER\x10\x01\x12\x1c\n\x18\x43RAS_NODE_TYPE_HEADPHONE\x10\x02\x12\x17\n\x13\x43RAS_NODE_TYPE_HDMI\x10\x03\x12\x19\n\x15\x43RAS_NODE_TYPE_HAPTIC\x10\x04\x12\x1f\n\x1b\x43RAS_NODE_TYPE_INTERNAL_MIC\x10\x05\x12\x1c\n\x18\x43RAS_NODE_TYPE_FRONT_MIC\x10\x06\x12\x1b\n\x17\x43RAS_NODE_TYPE_REAR_MIC\x10\x07\x12\x1f\n\x1b\x43RAS_NODE_TYPE_KEYBOARD_MIC\x10\x08\x12\x16\n\x12\x43RAS_NODE_TYPE_MIC\x10\t\x12\x1a\n\x16\x43RAS_NODE_TYPE_HOTWORD\x10\n\x12\x1a\n\x16\x43RAS_NODE_TYPE_LINEOUT\x10\x0b\x12$\n CRAS_NODE_TYPE_POST_MIX_LOOPBACK\x10\x0c\x12$\n CRAS_NODE_TYPE_POST_DSP_LOOPBACK\x10\r\x12,\n(CRAS_NODE_TYPE_POST_DSP_DELAYED_LOOPBACK\x10\x0e\x12\x16\n\x12\x43RAS_NODE_TYPE_USB\x10\x0f\x12\x1c\n\x18\x43RAS_NODE_TYPE_BLUETOOTH\x10\x10\x12#\n\x1f\x43RAS_NODE_TYPE_BLUETOOTH_NB_MIC\x10\x11\x12\"\n\x1e\x43RAS_NODE_TYPE_FALLBACK_NORMAL\x10\x12\x12$\n CRAS_NODE_TYPE_FALLBACK_ABNORMAL\x10\x13\x12!\n\x1d\x43RAS_NODE_TYPE_ECHO_REFERENCE\x10\x14\x12 \n\x1c\x43RAS_NODE_TYPE_ALSA_LOOPBACK\x10\x15\x12$\n CRAS_NODE_TYPE_FLEXIBLE_LOOPBACK\x10\x16\x12-\n)CRAS_NODE_TYPE_FLEXIBLE_LOOPBACK_INTERNAL\x10\x17*-\n\rCrasIODevType\x12\x1c\n\x18\x43RAS_IO_DEV_TYPE_HOTWORD\x10\x00*\xe6\x01\n\x0e\x43rasStreamType\x12\x1c\n\x18\x43RAS_STREAM_TYPE_DEFAULT\x10\x00\x12\x1f\n\x1b\x43RAS_STREAM_TYPE_MULTIMEDIA\x10\x01\x12(\n$CRAS_STREAM_TYPE_VOICE_COMMUNICATION\x10\x02\x12\'\n#CRAS_STREAM_TYPE_SPEECH_RECOGNITION\x10\x03\x12\x1e\n\x1a\x43RAS_STREAM_TYPE_PRO_AUDIO\x10\x04\x12\"\n\x1e\x43RAS_STREAM_TYPE_ACCESSIBILITY\x10\x05*\x95\x02\n\x0e\x43rasClientType\x12\x1c\n\x18\x43RAS_CLIENT_TYPE_UNKNOWN\x10\x00\x12\x1b\n\x17\x43RAS_CLIENT_TYPE_LEGACY\x10\x01\x12\x19\n\x15\x43RAS_CLIENT_TYPE_TEST\x10\x02\x12\x18\n\x14\x43RAS_CLIENT_TYPE_PCM\x10\x03\x12\x1b\n\x17\x43RAS_CLIENT_TYPE_CHROME\x10\x04\x12\x18\n\x14\x43RAS_CLIENT_TYPE_ARC\x10\x05\x12\x1b\n\x17\x43RAS_CLIENT_TYPE_CROSVM\x10\x06\x12\"\n\x1e\x43RAS_CLIENT_TYPE_SERVER_STREAM\x10\x07\x12\x1b\n\x17\x43RAS_CLIENT_TYPE_LACROS\x10\x08*\x99\x02\n\x12\x43rasConnectionType\x12 \n\x1c\x43RAS_CONNECTION_TYPE_CONTROL\x10\x00\x12!\n\x1d\x43RAS_CONNECTION_TYPE_PLAYBACK\x10\x01\x12 \n\x1c\x43RAS_CONNECTION_TYPE_CAPTURE\x10\x02\x12#\n\x1f\x43RAS_CONNECTION_TYPE_VMS_LEGACY\x10\x03\x12$\n CRAS_CONNECTION_TYPE_VMS_UNIFIED\x10\x04\x12(\n$CRAS_CONNECTION_TYPE_PLUGIN_PLAYBACK\x10\x05\x12\'\n#CRAS_CONNECTION_TYPE_PLUGIN_UNIFIED\x10\x06*r\n\x0cSampleFormat\x12\x14\n\x10SAMPLE_FORMAT_U8\x10\x00\x12\x18\n\x14SAMPLE_FORMAT_S16_LE\x10\x01\x12\x18\n\x14SAMPLE_FORMAT_S24_LE\x10\x02\x12\x18\n\x14SAMPLE_FORMAT_S32_LE\x10\x03*\xe2\x01\n\rCaptureEffect\x12\x16\n\x12\x43\x41PTURE_EFFECT_AEC\x10\x00\x12\x15\n\x11\x43\x41PTURE_EFFECT_NS\x10\x01\x12\x16\n\x12\x43\x41PTURE_EFFECT_AGC\x10\x02\x12\x16\n\x12\x43\x41PTURE_EFFECT_VAD\x10\x03\x12%\n!CAPTURE_EFFECT_AEC_ON_DSP_ALLOWED\x10\x04\x12$\n CAPTURE_EFFECT_NS_ON_DSP_ALLOWED\x10\x05\x12%\n!CAPTURE_EFFECT_AGC_ON_DSP_ALLOWED\x10\x06*\x88\x01\n\x17\x43rasIODevLastOpenResult\x12#\n\x1fIO_DEV_LAST_OPEN_RESULT_UNKNOWN\x10\x00\x12#\n\x1fIO_DEV_LAST_OPEN_RESULT_SUCCESS\x10\x01\x12#\n\x1fIO_DEV_LAST_OPEN_RESULT_FAILURE\x10\x02\x42\x35Z3go.chromium.org/tast-tests/cros/services/cros/audiob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tast.cros.services.cros.audio.cras_types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z3go.chromium.org/tast-tests/cros/services/cros/audio'
  _globals['_CRASNODETYPE']._serialized_start=268
  _globals['_CRASNODETYPE']._serialized_end=1075
  _globals['_CRASIODEVTYPE']._serialized_start=1077
  _globals['_CRASIODEVTYPE']._serialized_end=1122
  _globals['_CRASSTREAMTYPE']._serialized_start=1125
  _globals['_CRASSTREAMTYPE']._serialized_end=1355
  _globals['_CRASCLIENTTYPE']._serialized_start=1358
  _globals['_CRASCLIENTTYPE']._serialized_end=1635
  _globals['_CRASCONNECTIONTYPE']._serialized_start=1638
  _globals['_CRASCONNECTIONTYPE']._serialized_end=1919
  _globals['_SAMPLEFORMAT']._serialized_start=1921
  _globals['_SAMPLEFORMAT']._serialized_end=2035
  _globals['_CAPTUREEFFECT']._serialized_start=2038
  _globals['_CAPTUREEFFECT']._serialized_end=2264
  _globals['_CRASIODEVLASTOPENRESULT']._serialized_start=2267
  _globals['_CRASIODEVLASTOPENRESULT']._serialized_end=2403
  _globals['_CRASNODEID']._serialized_start=67
  _globals['_CRASNODEID']._serialized_end=119
  _globals['_CRASNODE']._serialized_start=122
  _globals['_CRASNODE']._serialized_end=265
# @@protoc_insertion_point(module_scope)

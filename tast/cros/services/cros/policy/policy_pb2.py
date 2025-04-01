# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tast/cros/services/cros/policy/policy.proto
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
    'tast/cros/services/cros/policy/policy.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+tast/cros/services/cros/policy/policy.proto\x12\x10tast.cros.policy\x1a\x1bgoogle/protobuf/empty.proto\"-\n\x19VerifyPolicyStatusRequest\x12\x10\n\x08policies\x18\x01 \x01(\x0c\"\xaf\x01\n\x18\x45nrollUsingChromeRequest\x12\x13\n\x0bpolicy_json\x18\x01 \x01(\x0c\x12\x10\n\x08username\x18\x02 \x01(\t\x12/\n\nextensions\x18\x03 \x03(\x0b\x32\x1b.tast.cros.policy.Extension\x12\x12\n\nextra_args\x18\x04 \x01(\t\x12\x13\n\x0b\x66\x61kedms_dir\x18\x05 \x01(\t\x12\x12\n\nskip_login\x18\x06 \x01(\x08\"M\n!ZeroTouchEnrollUsingChromeRequest\x12\x13\n\x0b\x64mserverURL\x18\x01 \x01(\t\x12\x13\n\x0bmanifestKey\x18\x02 \x01(\t\"J\n\x1e\x41utoReEnrollUsingChromeRequest\x12\x13\n\x0b\x64mserverURL\x18\x01 \x01(\t\x12\x13\n\x0bmanifestKey\x18\x02 \x01(\t\"N\n\"TokenBasedEnrollUsingChromeRequest\x12\x13\n\x0b\x64mserverURL\x18\x01 \x01(\t\x12\x13\n\x0bmanifestKey\x18\x02 \x01(\t\"W\n\x1cGAIAEnrollUsingChromeRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x13\n\x0b\x64mserverURL\x18\x03 \x01(\t\"_\n$GAIAEnrollAndLoginUsingChromeRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x13\n\x0b\x64mserverURL\x18\x03 \x01(\t\"\xb9\x01\n\x1dGAIAEnrollForReportingRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x14\n\x0c\x64mserver_url\x18\x03 \x01(\t\x12\x1c\n\x14reporting_server_url\x18\x04 \x01(\t\x12\x18\n\x10\x65nabled_features\x18\x05 \x01(\t\x12\x12\n\nextra_args\x18\x06 \x01(\t\x12\x12\n\nskip_login\x18\x07 \x01(\x08\"\xa4\x01\n\x1cGAIALoginForReportingRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x14\n\x0c\x64mserver_url\x18\x03 \x01(\t\x12\x1c\n\x14reporting_server_url\x18\x04 \x01(\t\x12\x18\n\x10\x65nabled_features\x18\x05 \x01(\t\x12\x12\n\nextra_args\x18\x06 \x01(\t\"^\n#SAMLTestIdPEnrollUsingChromeRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x13\n\x0b\x64mserverURL\x18\x03 \x01(\t\"\'\n\x17\x43reateFakeDMSDirRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\"+\n\x1b\x43reateTempFakeDMSDirRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\",\n\x1c\x43reateTempFakeDMSDirResponse\x12\x0c\n\x04path\x18\x01 \x01(\t\"\'\n\x17RemoveFakeDMSDirRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\",\n\x15UpdatePoliciesRequest\x12\x13\n\x0bpolicy_json\x18\x01 \x01(\x0c\"*\n\x16ServePolicyDataRequest\x12\x10\n\x08\x63ontents\x18\x01 \x01(\x0c\"4\n\x17ServePolicyDataResponse\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0c\n\x04hash\x18\x02 \x01(\t\"B\n\x16\x45valInExtensionRequest\x12\x14\n\x0c\x65xtension_id\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\")\n\x17\x45valInExtensionResponse\x12\x0e\n\x06result\x18\x01 \x01(\x0c\"/\n\rExtensionFile\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08\x63ontents\x18\x02 \x01(\x0c\"G\n\tExtension\x12\n\n\x02id\x18\x01 \x01(\t\x12.\n\x05\x66iles\x18\x02 \x03(\x0b\x32\x1f.tast.cros.policy.ExtensionFile\";\n VerifyVisibleNotificationRequest\x12\x17\n\x0fnotification_id\x18\x01 \x01(\t\"C\n EvalExpressionInChromeUrlRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x12\n\nexpression\x18\x02 \x01(\t\"}\n\x12StartChromeRequest\x12\x13\n\x0bpolicy_json\x18\x01 \x01(\x0c\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x12\n\nskip_login\x18\x03 \x01(\x08\x12\x17\n\x0fkeep_enrollment\x18\x04 \x01(\x08\x12\x13\n\x0b\x64\x65\x66\x65r_login\x18\x05 \x01(\x08\"$\n\x10\x43lientIdResponse\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\"0\n\x16\x44irectoryAPIIDResponse\x12\x16\n\x0e\x64irectoryAPIID\x18\x01 \x01(\t\"C\n\x1b\x44\x65viceAndCustomerIDResponse\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\t\x12\x12\n\ncustomerID\x18\x02 \x01(\t\":\n\x1aStableDeviceSecretResponse\x12\x1c\n\x14stable_device_secret\x18\x01 \x01(\t\"E\n\x1fUnlockDeviceWithPasswordRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"2\n\x18SendRemoteCommandRequest\x12\x16\n\x0eremote_command\x18\x01 \x01(\x0c\"/\n\x19SendRemoteCommandResponse\x12\x12\n\ncommand_id\x18\x01 \x01(\x03\"4\n\x1eWaitRemoteCommandResultRequest\x12\x12\n\ncommand_id\x18\x01 \x01(\x03\"1\n\x1fWaitRemoteCommandResultResponse\x12\x0e\n\x06result\x18\x01 \x01(\x0c\"3\n\x1dWaitRemoteCommandAckedRequest\x12\x12\n\ncommand_id\x18\x01 \x01(\x03\x32\xf1\x1c\n\rPolicyService\x12[\n\x12VerifyPolicyStatus\x12+.tast.cros.policy.VerifyPolicyStatusRequest\x1a\x16.google.protobuf.Empty\"\x00\x12H\n\x14StartNewChromeReader\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12J\n\x16WaitForEnrollmentError\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12k\n\x1aZeroTouchEnrollUsingChrome\x12\x33.tast.cros.policy.ZeroTouchEnrollUsingChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x65\n\x17\x41utoReEnrollUsingChrome\x12\x30.tast.cros.policy.AutoReEnrollUsingChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12m\n\x1bTokenBasedEnrollUsingChrome\x12\x34.tast.cros.policy.TokenBasedEnrollUsingChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12Y\n\x11\x45nrollUsingChrome\x12*.tast.cros.policy.EnrollUsingChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x61\n\x15GAIAEnrollUsingChrome\x12..tast.cros.policy.GAIAEnrollUsingChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12q\n\x1dGAIAEnrollAndLoginUsingChrome\x12\x36.tast.cros.policy.GAIAEnrollAndLoginUsingChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x63\n\x16GAIAEnrollForReporting\x12/.tast.cros.policy.GAIAEnrollForReportingRequest\x1a\x16.google.protobuf.Empty\"\x00\x12\x61\n\x15GAIALoginForReporting\x12..tast.cros.policy.GAIALoginForReportingRequest\x1a\x16.google.protobuf.Empty\"\x00\x12o\n\x1cSAMLTestIdPEnrollUsingChrome\x12\x35.tast.cros.policy.SAMLTestIdPEnrollUsingChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12S\n\x0eUpdatePolicies\x12\'.tast.cros.policy.UpdatePoliciesRequest\x1a\x16.google.protobuf.Empty\"\x00\x12I\n\x15\x43heckChromeAndFakeDMS\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12H\n\x14StopChromeAndFakeDMS\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12M\n\x0bStartChrome\x12$.tast.cros.policy.StartChromeRequest\x1a\x16.google.protobuf.Empty\"\x00\x12>\n\nStopChrome\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\x41\n\rContinueLogin\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12W\n\x10\x43reateFakeDMSDir\x12).tast.cros.policy.CreateFakeDMSDirRequest\x1a\x16.google.protobuf.Empty\"\x00\x12w\n\x14\x43reateTempFakeDMSDir\x12-.tast.cros.policy.CreateTempFakeDMSDirRequest\x1a..tast.cros.policy.CreateTempFakeDMSDirResponse\"\x00\x12W\n\x10RemoveFakeDMSDir\x12).tast.cros.policy.RemoveFakeDMSDirRequest\x1a\x16.google.protobuf.Empty\"\x00\x12K\n\x17StartExternalDataServer\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12h\n\x0fServePolicyData\x12(.tast.cros.policy.ServePolicyDataRequest\x1a).tast.cros.policy.ServePolicyDataResponse\"\x00\x12J\n\x16StopExternalDataServer\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12^\n\x18\x45valStatementInExtension\x12(.tast.cros.policy.EvalInExtensionRequest\x1a\x16.google.protobuf.Empty\"\x00\x12h\n\x0f\x45valInExtension\x12(.tast.cros.policy.EvalInExtensionRequest\x1a).tast.cros.policy.EvalInExtensionResponse\"\x00\x12i\n\x19VerifyVisibleNotification\x12\x32.tast.cros.policy.VerifyVisibleNotificationRequest\x1a\x16.google.protobuf.Empty\"\x00\x12i\n\x19\x45valExpressionInChromeURL\x12\x32.tast.cros.policy.EvalExpressionInChromeUrlRequest\x1a\x16.google.protobuf.Empty\"\x00\x12H\n\x08\x43lientID\x12\x16.google.protobuf.Empty\x1a\".tast.cros.policy.ClientIdResponse\"\x00\x12T\n\x0e\x44irectoryAPIID\x12\x16.google.protobuf.Empty\x1a(.tast.cros.policy.DirectoryAPIIDResponse\"\x00\x12^\n\x13\x44\x65viceAndCustomerID\x12\x16.google.protobuf.Empty\x1a-.tast.cros.policy.DeviceAndCustomerIDResponse\"\x00\x12\\\n\x12StableDeviceSecret\x12\x16.google.protobuf.Empty\x1a,.tast.cros.policy.StableDeviceSecretResponse\"\x00\x12>\n\nLockDevice\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12g\n\x18UnlockDeviceWithPassword\x12\x31.tast.cros.policy.UnlockDeviceWithPasswordRequest\x1a\x16.google.protobuf.Empty\"\x00\x12:\n\x06Logout\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12n\n\x11SendRemoteCommand\x12*.tast.cros.policy.SendRemoteCommandRequest\x1a+.tast.cros.policy.SendRemoteCommandResponse\"\x00\x12\x80\x01\n\x17WaitRemoteCommandResult\x12\x30.tast.cros.policy.WaitRemoteCommandResultRequest\x1a\x31.tast.cros.policy.WaitRemoteCommandResultResponse\"\x00\x12\x63\n\x16WaitRemoteCommandAcked\x12/.tast.cros.policy.WaitRemoteCommandAckedRequest\x1a\x16.google.protobuf.Empty\"\x00\x12I\n\x15RefreshRemoteCommands\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12P\n\x1c\x46indAndClickRestartNowButton\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x42\x36Z4go.chromium.org/tast-tests/cros/services/cros/policyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tast.cros.services.cros.policy.policy_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z4go.chromium.org/tast-tests/cros/services/cros/policy'
  _globals['_VERIFYPOLICYSTATUSREQUEST']._serialized_start=94
  _globals['_VERIFYPOLICYSTATUSREQUEST']._serialized_end=139
  _globals['_ENROLLUSINGCHROMEREQUEST']._serialized_start=142
  _globals['_ENROLLUSINGCHROMEREQUEST']._serialized_end=317
  _globals['_ZEROTOUCHENROLLUSINGCHROMEREQUEST']._serialized_start=319
  _globals['_ZEROTOUCHENROLLUSINGCHROMEREQUEST']._serialized_end=396
  _globals['_AUTOREENROLLUSINGCHROMEREQUEST']._serialized_start=398
  _globals['_AUTOREENROLLUSINGCHROMEREQUEST']._serialized_end=472
  _globals['_TOKENBASEDENROLLUSINGCHROMEREQUEST']._serialized_start=474
  _globals['_TOKENBASEDENROLLUSINGCHROMEREQUEST']._serialized_end=552
  _globals['_GAIAENROLLUSINGCHROMEREQUEST']._serialized_start=554
  _globals['_GAIAENROLLUSINGCHROMEREQUEST']._serialized_end=641
  _globals['_GAIAENROLLANDLOGINUSINGCHROMEREQUEST']._serialized_start=643
  _globals['_GAIAENROLLANDLOGINUSINGCHROMEREQUEST']._serialized_end=738
  _globals['_GAIAENROLLFORREPORTINGREQUEST']._serialized_start=741
  _globals['_GAIAENROLLFORREPORTINGREQUEST']._serialized_end=926
  _globals['_GAIALOGINFORREPORTINGREQUEST']._serialized_start=929
  _globals['_GAIALOGINFORREPORTINGREQUEST']._serialized_end=1093
  _globals['_SAMLTESTIDPENROLLUSINGCHROMEREQUEST']._serialized_start=1095
  _globals['_SAMLTESTIDPENROLLUSINGCHROMEREQUEST']._serialized_end=1189
  _globals['_CREATEFAKEDMSDIRREQUEST']._serialized_start=1191
  _globals['_CREATEFAKEDMSDIRREQUEST']._serialized_end=1230
  _globals['_CREATETEMPFAKEDMSDIRREQUEST']._serialized_start=1232
  _globals['_CREATETEMPFAKEDMSDIRREQUEST']._serialized_end=1275
  _globals['_CREATETEMPFAKEDMSDIRRESPONSE']._serialized_start=1277
  _globals['_CREATETEMPFAKEDMSDIRRESPONSE']._serialized_end=1321
  _globals['_REMOVEFAKEDMSDIRREQUEST']._serialized_start=1323
  _globals['_REMOVEFAKEDMSDIRREQUEST']._serialized_end=1362
  _globals['_UPDATEPOLICIESREQUEST']._serialized_start=1364
  _globals['_UPDATEPOLICIESREQUEST']._serialized_end=1408
  _globals['_SERVEPOLICYDATAREQUEST']._serialized_start=1410
  _globals['_SERVEPOLICYDATAREQUEST']._serialized_end=1452
  _globals['_SERVEPOLICYDATARESPONSE']._serialized_start=1454
  _globals['_SERVEPOLICYDATARESPONSE']._serialized_end=1506
  _globals['_EVALINEXTENSIONREQUEST']._serialized_start=1508
  _globals['_EVALINEXTENSIONREQUEST']._serialized_end=1574
  _globals['_EVALINEXTENSIONRESPONSE']._serialized_start=1576
  _globals['_EVALINEXTENSIONRESPONSE']._serialized_end=1617
  _globals['_EXTENSIONFILE']._serialized_start=1619
  _globals['_EXTENSIONFILE']._serialized_end=1666
  _globals['_EXTENSION']._serialized_start=1668
  _globals['_EXTENSION']._serialized_end=1739
  _globals['_VERIFYVISIBLENOTIFICATIONREQUEST']._serialized_start=1741
  _globals['_VERIFYVISIBLENOTIFICATIONREQUEST']._serialized_end=1800
  _globals['_EVALEXPRESSIONINCHROMEURLREQUEST']._serialized_start=1802
  _globals['_EVALEXPRESSIONINCHROMEURLREQUEST']._serialized_end=1869
  _globals['_STARTCHROMEREQUEST']._serialized_start=1871
  _globals['_STARTCHROMEREQUEST']._serialized_end=1996
  _globals['_CLIENTIDRESPONSE']._serialized_start=1998
  _globals['_CLIENTIDRESPONSE']._serialized_end=2034
  _globals['_DIRECTORYAPIIDRESPONSE']._serialized_start=2036
  _globals['_DIRECTORYAPIIDRESPONSE']._serialized_end=2084
  _globals['_DEVICEANDCUSTOMERIDRESPONSE']._serialized_start=2086
  _globals['_DEVICEANDCUSTOMERIDRESPONSE']._serialized_end=2153
  _globals['_STABLEDEVICESECRETRESPONSE']._serialized_start=2155
  _globals['_STABLEDEVICESECRETRESPONSE']._serialized_end=2213
  _globals['_UNLOCKDEVICEWITHPASSWORDREQUEST']._serialized_start=2215
  _globals['_UNLOCKDEVICEWITHPASSWORDREQUEST']._serialized_end=2284
  _globals['_SENDREMOTECOMMANDREQUEST']._serialized_start=2286
  _globals['_SENDREMOTECOMMANDREQUEST']._serialized_end=2336
  _globals['_SENDREMOTECOMMANDRESPONSE']._serialized_start=2338
  _globals['_SENDREMOTECOMMANDRESPONSE']._serialized_end=2385
  _globals['_WAITREMOTECOMMANDRESULTREQUEST']._serialized_start=2387
  _globals['_WAITREMOTECOMMANDRESULTREQUEST']._serialized_end=2439
  _globals['_WAITREMOTECOMMANDRESULTRESPONSE']._serialized_start=2441
  _globals['_WAITREMOTECOMMANDRESULTRESPONSE']._serialized_end=2490
  _globals['_WAITREMOTECOMMANDACKEDREQUEST']._serialized_start=2492
  _globals['_WAITREMOTECOMMANDACKEDREQUEST']._serialized_end=2543
  _globals['_POLICYSERVICE']._serialized_start=2546
  _globals['_POLICYSERVICE']._serialized_end=6243
# @@protoc_insertion_point(module_scope)

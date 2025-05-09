# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from tast.cros.services.cros.bluetooth import oobe_hid_bluetooth_service_pb2 as tast_dot_cros_dot_services_dot_cros_dot_bluetooth_dot_oobe__hid__bluetooth__service__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in tast/cros/services/cros/bluetooth/oobe_hid_bluetooth_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class OobeHidBluetoothServiceStub(object):
    """OobeHidBluetoothService allows bluetooth remote tests make calls to local,
    bluetooth-specific functions necessary for testing bluetooth features.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NewChrome = channel.unary_unary(
                '/tast.cros.bluetooth.OobeHidBluetoothService/NewChrome',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_bluetooth_dot_oobe__hid__bluetooth__service__pb2.NewChromeRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.CloseChrome = channel.unary_unary(
                '/tast.cros.bluetooth.OobeHidBluetoothService/CloseChrome',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.ProgressToWelcomeScreen = channel.unary_unary(
                '/tast.cros.bluetooth.OobeHidBluetoothService/ProgressToWelcomeScreen',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.DisableBluetoothFromQuickSettings = channel.unary_unary(
                '/tast.cros.bluetooth.OobeHidBluetoothService/DisableBluetoothFromQuickSettings',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.VerifyBluetoothIsEnabled = channel.unary_unary(
                '/tast.cros.bluetooth.OobeHidBluetoothService/VerifyBluetoothIsEnabled',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)


class OobeHidBluetoothServiceServicer(object):
    """OobeHidBluetoothService allows bluetooth remote tests make calls to local,
    bluetooth-specific functions necessary for testing bluetooth features.
    """

    def NewChrome(self, request, context):
        """NewChrome starts new chrome session in oobe, verifies that HID detection screen
        is shown. CloseChrome must be called later to clean up the associated resources.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CloseChrome(self, request, context):
        """CloseChrome releases the resources obtained by NewChrome.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProgressToWelcomeScreen(self, request, context):
        """ProgressToWelcomeScreen Progresses from Oobe HID screen to welcome screen.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisableBluetoothFromQuickSettings(self, request, context):
        """DisableBluetoothFromQuickSettings powers off the bluetooth adapter from quick settings.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyBluetoothIsEnabled(self, request, context):
        """VerifyBluetoothIsEnabled verifies Bluetooth is enabled and mouse device is connected.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OobeHidBluetoothServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NewChrome': grpc.unary_unary_rpc_method_handler(
                    servicer.NewChrome,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_bluetooth_dot_oobe__hid__bluetooth__service__pb2.NewChromeRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'CloseChrome': grpc.unary_unary_rpc_method_handler(
                    servicer.CloseChrome,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ProgressToWelcomeScreen': grpc.unary_unary_rpc_method_handler(
                    servicer.ProgressToWelcomeScreen,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'DisableBluetoothFromQuickSettings': grpc.unary_unary_rpc_method_handler(
                    servicer.DisableBluetoothFromQuickSettings,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'VerifyBluetoothIsEnabled': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyBluetoothIsEnabled,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tast.cros.bluetooth.OobeHidBluetoothService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('tast.cros.bluetooth.OobeHidBluetoothService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class OobeHidBluetoothService(object):
    """OobeHidBluetoothService allows bluetooth remote tests make calls to local,
    bluetooth-specific functions necessary for testing bluetooth features.
    """

    @staticmethod
    def NewChrome(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tast.cros.bluetooth.OobeHidBluetoothService/NewChrome',
            tast_dot_cros_dot_services_dot_cros_dot_bluetooth_dot_oobe__hid__bluetooth__service__pb2.NewChromeRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CloseChrome(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tast.cros.bluetooth.OobeHidBluetoothService/CloseChrome',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ProgressToWelcomeScreen(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tast.cros.bluetooth.OobeHidBluetoothService/ProgressToWelcomeScreen',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DisableBluetoothFromQuickSettings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tast.cros.bluetooth.OobeHidBluetoothService/DisableBluetoothFromQuickSettings',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def VerifyBluetoothIsEnabled(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tast.cros.bluetooth.OobeHidBluetoothService/VerifyBluetoothIsEnabled',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

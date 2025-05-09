# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from tast.cros.services.cros.ui import audio_service_pb2 as tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2

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
        + f' but the generated code in tast/cros/services/cros/ui/audio_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AudioServiceStub(object):
    """AudioService provides RPC methods to run audio-related operations.

    Prior to using this service, the ChromeService should be used to start
    the Chrome UI with ChromeService.New().
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.New = channel.unary_unary(
                '/tast.cros.ui.AudioService/New',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.Close = channel.unary_unary(
                '/tast.cros.ui.AudioService/Close',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.OpenDirectoryAndFile = channel.unary_unary(
                '/tast.cros.ui.AudioService/OpenDirectoryAndFile',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.GenerateTestRawData = channel.unary_unary(
                '/tast.cros.ui.AudioService/GenerateTestRawData',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.ConvertRawToWav = channel.unary_unary(
                '/tast.cros.ui.AudioService/ConvertRawToWav',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.KeyboardAccel = channel.unary_unary(
                '/tast.cros.ui.AudioService/KeyboardAccel',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.AudioCrasSelectedInputDevice = channel.unary_unary(
                '/tast.cros.ui.AudioService/AudioCrasSelectedInputDevice',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.FromString,
                _registered_method=True)
        self.AudioCrasSelectedOutputDevice = channel.unary_unary(
                '/tast.cros.ui.AudioService/AudioCrasSelectedOutputDevice',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.FromString,
                _registered_method=True)
        self.VerifyFirstRunningDevice = channel.unary_unary(
                '/tast.cros.ui.AudioService/VerifyFirstRunningDevice',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.SetActiveNodeByType = channel.unary_unary(
                '/tast.cros.ui.AudioService/SetActiveNodeByType',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.DownloadsPath = channel.unary_unary(
                '/tast.cros.ui.AudioService/DownloadsPath',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.FromString,
                _registered_method=True)
        self.SetWBSEnabled = channel.unary_unary(
                '/tast.cros.ui.AudioService/SetWBSEnabled',
                request_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)


class AudioServiceServicer(object):
    """AudioService provides RPC methods to run audio-related operations.

    Prior to using this service, the ChromeService should be used to start
    the Chrome UI with ChromeService.New().
    """

    def New(self, request, context):
        """Deprecated: Use ChromeService.New() instead.
        New is no longer supported and will throw an error if called.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Close(self, request, context):
        """Deprecated: Use ChromeService.Close() instead.
        Close is no longer supported and will throw an error if called.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OpenDirectoryAndFile(self, request, context):
        """OpenDirectoryAndFile performs launching filesapp and opening particular
        file in given directory.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GenerateTestRawData(self, request, context):
        """GenerateTestRawData generates test raw data file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConvertRawToWav(self, request, context):
        """ConvertRawToWav will convert raw data file to wav file format.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def KeyboardAccel(self, request, context):
        """KeyboardAccel will create keyboard event and performs keyboard
        key press with Accel().
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AudioCrasSelectedInputDevice(self, request, context):
        """AudioCrasSelectedInputDevice will return selected audio device name
        and audio device type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AudioCrasSelectedOutputDevice(self, request, context):
        """AudioCrasSelectedOutputDevice will return selected audio device name
        and audio device type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyFirstRunningDevice(self, request, context):
        """VerifyFirstRunningDevice will check for audio routing device.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetActiveNodeByType(self, request, context):
        """SetActiveNodeByType will set the provided audio node as Active audio node.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DownloadsPath(self, request, context):
        """DownloadsPath returns the path to the Downloads folder of the current user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetWBSEnabled(self, request, context):
        """SetWBSEnabled sets whether WBS should be enabled in the audio server
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AudioServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'New': grpc.unary_unary_rpc_method_handler(
                    servicer.New,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'Close': grpc.unary_unary_rpc_method_handler(
                    servicer.Close,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'OpenDirectoryAndFile': grpc.unary_unary_rpc_method_handler(
                    servicer.OpenDirectoryAndFile,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GenerateTestRawData': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateTestRawData,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ConvertRawToWav': grpc.unary_unary_rpc_method_handler(
                    servicer.ConvertRawToWav,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'KeyboardAccel': grpc.unary_unary_rpc_method_handler(
                    servicer.KeyboardAccel,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'AudioCrasSelectedInputDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.AudioCrasSelectedInputDevice,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.SerializeToString,
            ),
            'AudioCrasSelectedOutputDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.AudioCrasSelectedOutputDevice,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.SerializeToString,
            ),
            'VerifyFirstRunningDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyFirstRunningDevice,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SetActiveNodeByType': grpc.unary_unary_rpc_method_handler(
                    servicer.SetActiveNodeByType,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'DownloadsPath': grpc.unary_unary_rpc_method_handler(
                    servicer.DownloadsPath,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.SerializeToString,
            ),
            'SetWBSEnabled': grpc.unary_unary_rpc_method_handler(
                    servicer.SetWBSEnabled,
                    request_deserializer=tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tast.cros.ui.AudioService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('tast.cros.ui.AudioService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AudioService(object):
    """AudioService provides RPC methods to run audio-related operations.

    Prior to using this service, the ChromeService should be used to start
    the Chrome UI with ChromeService.New().
    """

    @staticmethod
    def New(request,
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
            '/tast.cros.ui.AudioService/New',
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
    def Close(request,
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
            '/tast.cros.ui.AudioService/Close',
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
    def OpenDirectoryAndFile(request,
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
            '/tast.cros.ui.AudioService/OpenDirectoryAndFile',
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
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
    def GenerateTestRawData(request,
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
            '/tast.cros.ui.AudioService/GenerateTestRawData',
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
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
    def ConvertRawToWav(request,
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
            '/tast.cros.ui.AudioService/ConvertRawToWav',
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
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
    def KeyboardAccel(request,
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
            '/tast.cros.ui.AudioService/KeyboardAccel',
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
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
    def AudioCrasSelectedInputDevice(request,
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
            '/tast.cros.ui.AudioService/AudioCrasSelectedInputDevice',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.FromString,
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
    def AudioCrasSelectedOutputDevice(request,
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
            '/tast.cros.ui.AudioService/AudioCrasSelectedOutputDevice',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.FromString,
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
    def VerifyFirstRunningDevice(request,
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
            '/tast.cros.ui.AudioService/VerifyFirstRunningDevice',
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
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
    def SetActiveNodeByType(request,
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
            '/tast.cros.ui.AudioService/SetActiveNodeByType',
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
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
    def DownloadsPath(request,
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
            '/tast.cros.ui.AudioService/DownloadsPath',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceResponse.FromString,
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
    def SetWBSEnabled(request,
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
            '/tast.cros.ui.AudioService/SetWBSEnabled',
            tast_dot_cros_dot_services_dot_cros_dot_ui_dot_audio__service__pb2.AudioServiceRequest.SerializeToString,
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

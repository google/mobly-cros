# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from tast.cros.services.cros.inputs import stylus_service_pb2 as tast_dot_cros_dot_services_dot_cros_dot_inputs_dot_stylus__service__pb2

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
        + f' but the generated code in tast/cros/services/cros/inputs/stylus_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class StylusServiceStub(object):
    """StylusService provides functionality to query the stylus.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FindPhysicalStylus = channel.unary_unary(
                '/tast.cros.inputs.StylusService/FindPhysicalStylus',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=tast_dot_cros_dot_services_dot_cros_dot_inputs_dot_stylus__service__pb2.FindPhysicalStylusResponse.FromString,
                _registered_method=True)
        self.CheckPhysicalStylusBatteryLevel = channel.unary_unary(
                '/tast.cros.inputs.StylusService/CheckPhysicalStylusBatteryLevel',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.FindPhysicalStylusBatteryLevel = channel.unary_unary(
                '/tast.cros.inputs.StylusService/FindPhysicalStylusBatteryLevel',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=tast_dot_cros_dot_services_dot_cros_dot_inputs_dot_stylus__service__pb2.FindPhysicalStylusBatteryLevelResponse.FromString,
                _registered_method=True)


class StylusServiceServicer(object):
    """StylusService provides functionality to query the stylus.
    """

    def FindPhysicalStylus(self, request, context):
        """FindPhysicalStylus finds the /dev/input/event* file for a physical stylus.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckPhysicalStylusBatteryLevel(self, request, context):
        """CheckPhysicalStylusBatteryLevel checks that the stylus battery level is
        above a specific threshold.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindPhysicalStylusBatteryLevel(self, request, context):
        """FindPhysicalStylusBatteryLevel returns the battery level of
        a physical stylus if one is present.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StylusServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FindPhysicalStylus': grpc.unary_unary_rpc_method_handler(
                    servicer.FindPhysicalStylus,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=tast_dot_cros_dot_services_dot_cros_dot_inputs_dot_stylus__service__pb2.FindPhysicalStylusResponse.SerializeToString,
            ),
            'CheckPhysicalStylusBatteryLevel': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckPhysicalStylusBatteryLevel,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'FindPhysicalStylusBatteryLevel': grpc.unary_unary_rpc_method_handler(
                    servicer.FindPhysicalStylusBatteryLevel,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=tast_dot_cros_dot_services_dot_cros_dot_inputs_dot_stylus__service__pb2.FindPhysicalStylusBatteryLevelResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tast.cros.inputs.StylusService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('tast.cros.inputs.StylusService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class StylusService(object):
    """StylusService provides functionality to query the stylus.
    """

    @staticmethod
    def FindPhysicalStylus(request,
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
            '/tast.cros.inputs.StylusService/FindPhysicalStylus',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            tast_dot_cros_dot_services_dot_cros_dot_inputs_dot_stylus__service__pb2.FindPhysicalStylusResponse.FromString,
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
    def CheckPhysicalStylusBatteryLevel(request,
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
            '/tast.cros.inputs.StylusService/CheckPhysicalStylusBatteryLevel',
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
    def FindPhysicalStylusBatteryLevel(request,
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
            '/tast.cros.inputs.StylusService/FindPhysicalStylusBatteryLevel',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            tast_dot_cros_dot_services_dot_cros_dot_inputs_dot_stylus__service__pb2.FindPhysicalStylusBatteryLevelResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

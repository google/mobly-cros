# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

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
        + f' but the generated code in tast/cros/services/cros/policy/device_minimum_version_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DeviceMinimumVersionServiceStub(object):
    """DeviceMinimumVersionService provides functions to test the DeviceMinimumVersion policy.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TestUpdateRequiredScreenIsVisible = channel.unary_unary(
                '/tast.cros.policy.DeviceMinimumVersionService/TestUpdateRequiredScreenIsVisible',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)


class DeviceMinimumVersionServiceServicer(object):
    """DeviceMinimumVersionService provides functions to test the DeviceMinimumVersion policy.
    """

    def TestUpdateRequiredScreenIsVisible(self, request, context):
        """Creates a new instance of Chrome using the state from the existing one.
        Checks that an update required screen with update now button is visible on the login page.
        Chrome is closed when function exists. This is used by the test policy.DeviceMinimumVersion.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DeviceMinimumVersionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TestUpdateRequiredScreenIsVisible': grpc.unary_unary_rpc_method_handler(
                    servicer.TestUpdateRequiredScreenIsVisible,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tast.cros.policy.DeviceMinimumVersionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('tast.cros.policy.DeviceMinimumVersionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DeviceMinimumVersionService(object):
    """DeviceMinimumVersionService provides functions to test the DeviceMinimumVersion policy.
    """

    @staticmethod
    def TestUpdateRequiredScreenIsVisible(request,
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
            '/tast.cros.policy.DeviceMinimumVersionService/TestUpdateRequiredScreenIsVisible',
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

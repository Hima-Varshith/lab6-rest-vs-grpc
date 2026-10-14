import grpc
from concurrent import futures
import io
import base64
import argparse

from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):

    def Add(self, request, context):
        result = request.a + request.b

        return lab6_pb2.addReply(sum=result)

    def RawImage(self, request, context):
        try:
            image_buffer = io.BytesIO(request.img)
            img = Image.open(image_buffer)

            return lab6_pb2.imageReply(
                width=img.size[0],
                height=img.size[1]
            )

        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)

    def DotProduct(self, request, context):
        a = request.a
        b = request.b

        if len(a) != len(b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        result = sum(x * y for x, y in zip(a, b))

        return lab6_pb2.dotProductReply(dotproduct=result)

    def JsonImage(self, request, context):
        try:
            image_bytes = base64.b64decode(request.img, validate=True)
            image_buffer = io.BytesIO(image_bytes)
            img = Image.open(image_buffer)

            return lab6_pb2.imageReply(
                width=img.size[0],
                height=img.size[1]
            )

        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Service(), server
    )

    server.add_insecure_port(f'[::]:{port}')

    server.start()

    print(f"gRPC server running on port {port}")

    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="gRPC Server")

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=50051
    )

    args = parser.parse_args()

    serve(args.port)

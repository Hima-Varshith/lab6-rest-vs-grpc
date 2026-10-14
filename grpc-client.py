import grpc
import argparse
import random
import time
import base64

import lab6_pb2
import lab6_pb2_grpc


def doAdd(stub, debug=False):
    request = lab6_pb2.addMsg(a=5, b=10)
    response = stub.Add(request)

    if debug:
        print("Sum:", response.sum)


def doRawImage(stub, debug=False):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img = f.read()

    request = lab6_pb2.rawImageMsg(img=img)
    response = stub.RawImage(request)

    if debug:
        print("Width:", response.width)
        print("Height:", response.height)


def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    request = lab6_pb2.dotProductMsg(a=a, b=b)
    response = stub.DotProduct(request)

    if debug:
        print("Dot Product:", response.dotproduct)


def doJsonImage(stub, debug=False):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img = f.read()

    encoded_image = base64.b64encode(img).decode('utf-8')

    request = lab6_pb2.jsonImageMsg(img=encoded_image)
    response = stub.JsonImage(request)

    if debug:
        print("Width:", response.width)
        print("Height:", response.height)


def main():
    parser = argparse.ArgumentParser(
        description='gRPC client for measuring server operations'
    )

    parser.add_argument(
        'host',
        help='IP address or hostname of the gRPC server'
    )

    parser.add_argument(
        'cmd',
        choices=['add', 'rawImage', 'dotProduct', 'jsonImage'],
        help='Operation to perform'
    )

    parser.add_argument(
        'reps',
        type=int,
        help='Number of repetitions'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=50051,
        help='Server port (default: 50051)'
    )

    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Print server responses'
    )

    args = parser.parse_args()

    if args.reps <= 0:
        parser.error('reps must be greater than zero')

    addr = f'{args.host}:{args.port}'

    print(f'Running {args.reps} reps against {addr}')

    operations = {
        'add': doAdd,
        'rawImage': doRawImage,
        'dotProduct': doDotProduct,
        'jsonImage': doJsonImage
    }

    with grpc.insecure_channel(addr) as channel:
        stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

        grpc.channel_ready_future(channel).result(timeout=10)

        start = time.perf_counter()

        for _ in range(args.reps):
            operations[args.cmd](stub, debug=args.debug)

        delta = ((time.perf_counter() - start) / args.reps) * 1000

        print('Took', delta, 'ms per operation')


if __name__ == '__main__':
    main()

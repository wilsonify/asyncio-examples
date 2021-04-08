"""
Clean separation with zmq and asyncio

For the code examples that follow, it is necessary to use pyzmq >= 17.0.0. At the
time of writing, version 17 wasn’t released yet, so if necessary you will have to
install the latest beta of pyzmq with a major version of 17.
"""

import asyncio
import zmq
from zmq.asyncio import Context

context = Context()


async def do_receiver():
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")
    while True:
        message = await receiver.recv_json()
        print(f'Via PULL: {message}')


async def do_subscriber():
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5556")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
    while True:
        message = await subscriber.recv_json()
        print(f'Via SUB: {message}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(do_receiver())
    loop.create_task(do_subscriber())
    loop.run_forever()

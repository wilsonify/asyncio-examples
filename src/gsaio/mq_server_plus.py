"""
Example 4­9. Message broker: improved design
"""

import asyncio
from asyncio import StreamReader, StreamWriter, Queue
from collections import deque, defaultdict
from contextlib import suppress
from typing import Deque, DefaultDict, Dict
from msgproto import read_msg, send_msg, run_server

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)
SEND_QUEUES: DefaultDict[StreamWriter, Queue] = defaultdict(Queue)
CHAN_QUEUES: Dict[bytes, Queue] = {}


async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.transport.get_extra_info('peername')
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    loop = asyncio.get_event_loop()
    send_task = loop.create_task(
        send_client(writer, SEND_QUEUES[writer]))
    print(f'Remote {peername} subscribed to {subscribe_chan}')
    try:
        while True:
            channel_name = await read_msg(reader)
            data = await read_msg(reader)
            if channel_name not in CHAN_QUEUES:
                CHAN_QUEUES[channel_name] = Queue(maxsize=10)
                loop.create_task(chan_sender(channel_name))
            await CHAN_QUEUES[channel_name].put(data)
    except asyncio.CancelledError:
        print(f'Remote {peername} connection cancelled.')
    except asyncio.streams.IncompleteReadError:
        print(f'Remote {peername} disconnected')
    finally:
        print(f'Remote {peername} closed')
        await SEND_QUEUES[writer].put(None)
        await send_task
        del SEND_QUEUES[writer]
        SUBSCRIBERS[subscribe_chan].remove(writer)


async def send_client(writer: StreamWriter, queue: Queue):
    while True:
        with suppress(asyncio.CancelledError):
            data = await queue.get()
            if not data:
                writer.close()
                break
            await send_msg(writer, data)


async def chan_sender(name: bytes):
    with suppress(asyncio.CancelledError):
        while True:
            writers = SUBSCRIBERS[name]
            if not writers:
                await asyncio.sleep(1)
                continue
            if name.startswith(b'/queue'):
                writers.rotate(n=1)
                writers = [writers[0]]
                msg = await CHAN_QUEUES[name].get()
            if not msg:
                break
            for writer in writers:
                if not SEND_QUEUES[writer].full():
                    print(f'Sending to {name}: {msg[:19]}...')
                    await SEND_QUEUES[writer].put(msg)


if __name__ == '__main__':
    run_server(client)

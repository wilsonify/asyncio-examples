"""
A 35­line prototype
"""

import asyncio
from asyncio import StreamReader, StreamWriter, gather
from collections import deque, defaultdict
from typing import Deque, DefaultDict
from msgproto import read_msg, send_msg, run_server

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)


async def client(reader: StreamReader, writer: StreamWriter):
    peer_name = writer.transport.get_extra_info('peer_name')
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    print(f'Remote {peer_name} subscribed to {subscribe_chan}')
    try:
        while True:
            channel_name = await read_msg(reader)
            data = await read_msg(reader)
            print(f'Sending to {channel_name}: {data[:19]}...')
            writers = SUBSCRIBERS[channel_name]
            if writers and channel_name.startswith(b'/queue'):
                writers.rotate(n=1)
                writers = [writers[0]]
            await gather(*[send_msg(w, data) for w in writers])
    except asyncio.CancelledError:
        print(f'Remote {peer_name} closing connection.')
        writer.close()
    except asyncio.streams.IncompleteReadError:
        print(f'Remote {peer_name} disconnected')
    finally:
        print(f'Remote {peer_name} closed')
        SUBSCRIBERS[subscribe_chan].remove(writer)


if __name__ == '__main__':
    run_server(client)

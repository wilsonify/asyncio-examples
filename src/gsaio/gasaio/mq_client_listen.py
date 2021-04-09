"""
Listener: a toolkit for listening for messages on our message broker
"""

import asyncio
import argparse
import uuid
from msgproto import read_msg, send_msg


async def main(args):
    me = uuid.uuid4().hex[:8]
    print(f'Starting up {me}')
    reader, writer = await asyncio.open_connection(
        args.host,
        args.port
    )
    print(f'I am {writer.transport.get_extra_info("sockname")}')
    channel = args.listen.encode()
    await send_msg(writer, channel)
    try:
        while True:
            data = await read_msg(reader)
            if not data:
                print('Connection ended.')
                break
        print(f'Received by {me}: {data[:20]}')
    except asyncio.streams.IncompleteReadError:
        print('Server closed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('­­host', default='localhost')
    parser.add_argument('­­port', default=25000)
    parser.add_argument('­­listen', default='/topic/foo')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(parser.parse_args()))
    except KeyboardInterrupt:
        print('Bye!')
    loop.close()

"""
Sender: a toolkit for sending data to our message broker
"""
import asyncio
import argparse, uuid
from itertools import count
from msgproto import send_msg


async def main(args):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")
    reader, writer = await asyncio.open_connection(
        host=args.host,
        port=args.port
    )
    print(f'I am {writer.transport.get_extra_info("sockname")}')
    channel = b'/null'
    await send_msg(writer, channel)
    chan = args.channel.encode()
    for i in count():
        await asyncio.sleep(args.interval)
        data = b'X' * args.size or f'Msg {i} from {me}'.encode()
        try:
            await send_msg(writer, chan)
            await send_msg(writer, data)
        except ConnectionResetError:
            print('Connection ended.')
            break
    writer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('­­host', default='localhost')
    parser.add_argument('­­port', default=25000, type=int)
    parser.add_argument('­­channel', default='/topic/foo')
    parser.add_argument('­­interval', default=1, type=float)
    parser.add_argument('­­size', default=0, type=int)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(parser.parse_args()))
    except KeyboardInterrupt:
        print('Bye!')
    loop.close()

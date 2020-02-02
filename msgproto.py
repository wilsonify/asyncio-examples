"""
Message protocol: read and write
"""

import asyncio
from asyncio import StreamReader, StreamWriter


async def read_msg(reader: StreamReader) -> bytes:
    """
    # Raises asyncio.streams.IncompleteReadError
    :param reader:
    :return:
    """
    size_bytes = await reader.readexactly(4)
    size = int.from_bytes(size_bytes, byteorder='big')
    data = await reader.readexactly(size)
    return data


async def send_msg(writer: StreamWriter, data: bytes):
    """

    :param writer:
    :param data:
    :return:
    """
    writer.write(len(data).to_bytes(4, byteorder='big'))
    writer.write(data)
    await writer.drain()


def run_server(client, host='127.0.0.1', port=25000):
    """

    :param client:
    :param host:
    :param port:
    :return:
    """
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(client, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Bye!')
    server.close()
    loop.run_until_complete(server.wait_closed())
    tasks = asyncio.Task.all_tasks()
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()

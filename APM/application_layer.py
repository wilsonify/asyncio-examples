"""
Example 4­15. The application layer: producing metrics
"""

import argparse
import asyncio
from asyncio import get_event_loop, gather, sleep, CancelledError
from contextlib import suppress
from datetime import datetime as dt
from datetime import timezone as tz
from random import randint, uniform
from signal import SIGINT

import psutil
import zmq
import zmq.asyncio

# zmq.asyncio.install()
ctx = zmq.asyncio.Context()


async def stats_reporter(color: str):
    p = psutil.Process()
    sock = ctx.socket(zmq.PUB)
    sock.setsockopt(zmq.LINGER, 1)
    sock.connect('tcp://localhost:5555')
    with suppress(CancelledError):
        while True:
            await sock.send_json(dict(
                color=color,
                timestamp=dt.now(tz=tz.utc).isoformat(),
                cpu=p.cpu_percent(),
                mem=p.memory_full_info().rss / 1024 / 1024
            ))
            await sleep(1)
    # To end up here, we must have received the CancelledError exception resulting from
    # task cancellation. The ØMQ socket must be closed to allow program shutdown.
    sock.close()


async def main(args):
    leak = []
    with suppress(CancelledError):
        while True:
            sum(range(randint(1_000, 10_000_000)))
            await sleep(uniform(0, 1))
            leak += [0] * args.leak


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('­­color', type=str, default="red")
    parser.add_argument('­­leak', type=int, default=0)
    args = parser.parse_args()
    loop = get_event_loop()
    loop.add_signal_handler(SIGINT, loop.call_soon, loop.stop)
    tasks = gather(main(args), stats_reporter(args.color))
    loop.run_forever()
    print('Leaving...')
    for t in asyncio.Task.all_tasks():
        t.cancel()
    loop.run_until_complete(tasks)
    ctx.term()

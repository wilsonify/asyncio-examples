"""
Connect coroutines and threads with a Janus queue
"""

import asyncio, time, random, janus

loop = asyncio.get_event_loop()
queue = janus.Queue(loop=loop)


async def main():
    while True:
        data = await queue.async_q.get()
        if data is None:
            break
        print(f'Got {data} off queue')
    print('Done.')


def data_source():
    for i in range(10):
        r = random.randint(0, 4)
        time.sleep(r)
        queue.sync_q.put(r)
    queue.sync_q.put(None)


if __name__ == "__main__":
    loop.run_in_executor(None, data_source)
    loop.run_until_complete(main())
    loop.close()

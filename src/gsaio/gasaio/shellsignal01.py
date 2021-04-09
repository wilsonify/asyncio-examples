"""
using KeyboardInterrupt as SIGINT handler
"""

import asyncio


async def main():
    while True:
        print('<Your app is running>')
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Got signal: SIGINT, shutting down.')
    tasks = asyncio.Task.all_tasks()
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()

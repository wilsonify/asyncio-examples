"""
destroyer of pending tasks
"""
import asyncio


async def f(delay):
    await asyncio.sleep(delay)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(f(1))
    t2 = loop.create_task(f(2))
    loop.run_until_complete(t1)
    loop.close()

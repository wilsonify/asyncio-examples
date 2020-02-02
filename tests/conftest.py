import asyncio

import pytest


@pytest.fixture(scope='function')
def loop():
    """
    once set_event_loop() is called, every subsequent call to
    asyncio.get_event_loop() will return the loop instance created in this fixture, and
    you don’t have to explicitly pass the loop instance through all your function calls.
    :return:
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()

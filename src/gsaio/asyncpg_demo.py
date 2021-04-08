"""
 Basic demo of asyncpg
"""

import asyncio
import asyncpg
import datetime
from util import Database


async def main():
    async with Database('test', owner=True) as conn:
        await demo(conn)


async def demo(conn: asyncpg.Connection):
    await conn.execute(
        '''
            CREATE TABLE users(
                id serial PRIMARY KEY,
                name text,
                dob date
            )'''
    )
    pk = await conn.fetchval(
        'INSERT INTO users(name, dob) VALUES($1, $2) '
        'RETURNING id', 'Bob', datetime.date(1984, 3, 1)
    )

    async def get_row():
        return await conn.fetchrow(
            'SELECT * FROM users WHERE name = $1',
            'Bob'
        )

    print('After INSERT:', await get_row())
    await conn.execute(
        'UPDATE users SET dob = $1 WHERE id=1',
        datetime.date(1985, 3, 1)
    )
    print('After UPDATE:', await get_row())
    await conn.execute(
        'DELETE FROM users WHERE id=1'
    )
    print('After DELETE:', await get_row())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

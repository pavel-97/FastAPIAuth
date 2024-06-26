#Test settings

from typing import Final

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .env import POSTGRES_DB_TEST, POSTGRES_PASSWORD_TEST, POSTGRES_USER_TEST


DATABASE_URL_TEST: Final = f'postgresql+asyncpg://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}@db_test/{POSTGRES_DB_TEST}'


async_engine_test = create_async_engine(url=DATABASE_URL_TEST)
engine_test = create_engine(url=DATABASE_URL_TEST)
async_session_maker_test = async_sessionmaker(async_engine_test, expire_on_commit=False)
session_maker_test = sessionmaker(engine_test, expire_on_commit=False)


async def get_async_session_overrides():
    '''Async function to get test session object'''

    async with async_session_maker_test() as session:
        yield session

from typing import Final

from passlib.context import CryptContext

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from starlette_admin.contrib.sqla import Admin

from celery import Celery

from .env import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, SECRET_KEY, RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_USER


DATABASE_URL: Final = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db_user/{POSTGRES_DB}'


async_engine = create_async_engine(DATABASE_URL)
async_engine.echo = True

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


#-----------------------------------------------------------------------------------------------------------


celery = Celery('tasks', broker=f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq', backend='redis://redis')


#-----------------------------------------------------------------------------------------------------------


admin = Admin(engine=async_engine, title='Example: SQLAlchemy')


#-----------------------------------------------------------------------------------------------------------


async def get_async_session():
    async with async_session_maker() as session:
        yield session

#-----------------------------------------------------------------------------------------------------------


access_security = JwtAccessBearer(secret_key=SECRET_KEY, auto_error=True)

refresh_security = JwtRefreshBearer(secret_key=SECRET_KEY, auto_error=True)


#-----------------------------------------------------------------------------------------------------------


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#-----------------------------------------------------------------------------------------------------------


class Base(DeclarativeBase):
    ...
    

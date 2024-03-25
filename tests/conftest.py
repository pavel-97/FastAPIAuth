#Test configurations

import pytest
import asyncio

from httpx import AsyncClient, Client

from src.settings import get_async_session, Base, get_password_hash
from src.main import app
from src.utils.unitofworks import AsyncUnitOfWork, UnitOfWork
from src.repositories.users import AsyncUserRepository
from src.services.users import UserService
from src.tasks import registry_task

from .settings import async_engine_test, get_async_session_overrides, async_session_maker_test, session_maker_test
from .schemas import TestSuperUser
from .consts import SUPER_USER_DATA, USER_DATA


Base.metadata.bind = async_engine_test
app.dependency_overrides[get_async_session] = get_async_session_overrides


class TestAsyncUnitOfWork(AsyncUnitOfWork):
    '''Class Test async unit of work with test DB'''

    def __init__(self) -> None:
        self.session_factory = async_session_maker_test


class TestUnitOfWork(UnitOfWork):
    '''Class Test unit of work with test DB'''

    def __init__(self) -> None:
        self.session_factory = session_maker_test


app.dependency_overrides[AsyncUnitOfWork] = TestAsyncUnitOfWork
app.dependency_overrides[UnitOfWork] = TestUnitOfWork


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    '''Fixture creates test tables in test DB'''

    async with async_engine_test.begin() as conn:
        async_engine_test.echo = True
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def async_client():
    '''Fixture creates test client'''

    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
def client():
    with Client(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
def registry():
    '''Fixture registries test user'''

    assert registry_task.delay(data=USER_DATA).get(timeout=10) == None
    # assert test_registry()


@pytest.fixture(scope='session')
async def create_super_user():
    '''Fixture creates test super user'''

    hashed_password = get_password_hash(SUPER_USER_DATA.pop('password'))
    async with TestAsyncUnitOfWork() as test_uow:
        (
        await AsyncUserRepository(session=test_uow.session).create(
            schema=TestSuperUser(
                hashed_password=hashed_password,
                **SUPER_USER_DATA
                )
            )
        )
        await test_uow.commit()

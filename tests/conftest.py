import pytest
import asyncio

from httpx import AsyncClient

from src.settings import get_async_session, Base, get_password_hash
from src.main import app
from src.utils.unitofworks import UnitOfWork
from src.repositories.users import UserRepository
from src.tasks import registry_task_test
from src.models import Role

from .settings import async_engine_test, get_async_session_overrides, async_session_maker_test
from .schemas import TestSuperUser


Base.metadata.bind = async_engine_test
app.dependency_overrides[get_async_session] = get_async_session_overrides


class TestUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker_test


app.dependency_overrides[UnitOfWork] = TestUnitOfWork


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
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
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def registry(async_client: AsyncClient):
    assert registry_task_test.delay(data={
        'email': 'test_user_2@mail.com',
        'password': 'test_pwd',
        'role': ["user", ],
    }).get(timeout=10) == None


@pytest.fixture(scope='session')
async def create_super_user():
    data_user = {
        'email': 'test_super_user@mail.com',
        'password': 'test_pwd',
        'role': [Role.super_user]
    }
    hashed_password = get_password_hash(data_user.pop('password'))
    test_uow = TestUnitOfWork()
    async with test_uow:
        user = (
            await UserRepository(
            session=test_uow.session
                ).
                create(schema=TestSuperUser(
                    hashed_password=hashed_password,
                    **data_user
                        )
                    )
            )
        await test_uow.commit()



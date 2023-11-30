import pytest
import asyncio

from httpx import AsyncClient

from src.settings import get_async_session, Base
from src.main import app
from src.utils.unitofworks import UnitOfWork

from .settings import async_engine_test, get_async_session_overrides, async_session_maker_test


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


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def async_client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
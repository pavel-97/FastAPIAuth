import asyncio

from celery import Task

from src.utils.unitofworks import UnitOfWork
from src.services.users import UserService

from .settings import celery


class CeleryTask(Task):
    def __init__(self) -> None:
        super().__init__()
        self.uow = UnitOfWork()


async def registry_corutine(uow, data):
    await UserService().registry(uow=uow, registry_user=data)


@celery.task(bind=True, base=CeleryTask)
def registry_task(self, data):
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(registry_corutine(self.uow, data))
    # asyncio.run(registry_corutine(self.uow, data))


#----------Testing Celery-------------------------------------------------------------------------------------------------

from tests.settings import async_session_maker_test


class CeleryTaskTest(Task):
    def __init__(self) -> None:
        super().__init__()
        self.uow = TestUnitOfWork()


class TestUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker_test


@celery.task(bind=True, base=CeleryTaskTest)
def registry_task_test(self, data):
    ioloop = asyncio.get_event_loop()
    task = ioloop.create_task(registry_corutine(self.uow, data))
    ioloop.run_until_complete(asyncio.wait([task, ]))
    # asyncio.run(registry_corutine(self.uow, data))

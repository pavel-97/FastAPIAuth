#Async process, tasks, celery

from celery import Task

from src.utils.unitofworks import UnitOfWork
from src.services.users import UserService

from .settings import celery


class CeleryTask(Task):
    def __init__(self) -> None:
        super().__init__()
        self.uow = UnitOfWork()


def registry(uow, data):
    res = UserService().registry(uow=uow, registry_user=data)
    print(res, '--*--'*10)


@celery.task(bind=True, base=CeleryTask)
def registry_task(self, data):
    res = UserService().registry(uow=self.uow, registry_user=data)
    print(res, '--*--'*10)

    # registry(self.uow, data=data)

#Async process, tasks, celery

from celery import Task # type: ignore [import-untyped]

from src.utils.unitofworks import UnitOfWork
from src.services.users import UserService

from .settings import celery


class RegistryTask(Task):
    
    def __init__(self) -> None:
        self.uow = UnitOfWork()


@celery.task(bind=True, base=RegistryTask)
def registry_task(self, registry_user: dict):

    with self.uow:
        UserService().registry(uow=self.uow, registry_user=registry_user)


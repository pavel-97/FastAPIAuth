from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import async_session_maker


class ABCUnitOfWork(ABC):

    @abstractmethod
    def __aenter__(self, *awrgs, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def commit(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def rollback(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def close(self, *args, **kwargs):
        raise NotImplementedError
    


class UnitOfWork(ABCUnitOfWork):
    
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self, *awrgs, **kwargs):
        self.session: AsyncSession = self.session_factory()
        return self
    
    async def __aexit__(self, type, value, traceback):
        await self.rollback()
        await self.close()

    async def commit(self, *args, **kwargs):
        return await self.session.commit(*args, **kwargs)

    async def rollback(self, *args, **kwargs):
        return await self.session.rollback(*args, **kwargs)
    
    async def close(self, *args, **kwargs):
        return await self.session.close(*args, **kwargs)
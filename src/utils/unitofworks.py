#Unit of work

from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.settings import async_session_maker, session_maker


class ABCUnitOfWork(ABC):
    '''Abstract class'''

    # @abstractmethod
    # def __aenter__(self, *awrgs, **kwargs):
        # '''Method without realization'''

        # raise NotImplementedError
    
    # @abstractmethod
    # def __aexit__(self, *args, **kwargs):
        # '''Method without realization'''

        # raise NotImplementedError

    @abstractmethod
    def commit(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    
    @abstractmethod
    def rollback(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    
    @abstractmethod
    def close(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    

class UnitOfWork(ABCUnitOfWork):
    '''Class unit of work'''
    
    def __init__(self):
        '''Constructor'''

        self.session_factory = session_maker

    def __enter__(self):
        '''Enter in context manager'''
        
        self.session: Session = self.session_factory()
        return self
    
    def __exit__(self, type, value, traceback):
        '''Exit from context manager'''

        self.rollback()
        self.close()

    def rollback(self, *args, **kwargs):
        '''Reset all changes'''

        return self.session.rollback(*args, **kwargs)
    
    def commit(self, *args, **kwargs):
        '''Save all changes'''

        self.session.commit(*args, **kwargs)
    
    def close(self, *args, **kwargs):
        '''Close DB session'''
        
        return self.session.close(*args, **kwargs)
    

class AsyncUnitOfWork(ABCUnitOfWork):
    '''Class async unit of work controls DB transatctions'''
    
    def __init__(self) -> None:
        '''Constructor'''

        self.session_factory = async_session_maker

    async def __aenter__(self, *awrgs, **kwargs):
        '''Enter in async context manager'''

        self.session: AsyncSession = self.session_factory()
        return self
    
    async def __aexit__(self, type, value, traceback):
        '''Exit from async context manager'''

        await self.rollback()
        await self.close()

    async def commit(self, *args, **kwargs):
        '''Save all changes in DB'''

        return await self.session.commit(*args, **kwargs)

    async def rollback(self, *args, **kwargs):
        '''Reset all changes'''

        return await self.session.rollback(*args, **kwargs)
    
    async def close(self, *args, **kwargs):
        '''Close DB session'''

        return await self.session.close(*args, **kwargs)
    
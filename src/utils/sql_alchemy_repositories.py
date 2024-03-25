#SQLAlchemy reposytory

from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from pydantic import BaseModel

from . repositories import ABCRepository


class SQLAlchemyReposytory(ABCRepository):
    '''Class SQLAlchemy Repository works with BD through SQLAlchemy'''

    model: DeclarativeBase

    def __init__(self, session: Session) -> None:
        self.session: Session = session
    
    def create(self, schema: BaseModel):
        '''Method creates object in DB'''

        new_obj = self.model(**schema.dict())
        self.session.add(new_obj)
        return new_obj


class AsyncSQLAlchemyReposytory(ABCRepository):
    '''Class Async SQLAlchemy Repository works with BD through SQLAlchemy'''

    model: DeclarativeBase

    def __init__(self, session: AsyncSession) -> None:
        '''Constructor'''

        self.session: AsyncSession = session

    async def get(self, id: int):
        '''Method returns object from DB by id'''

        # stml = select(self.model).where(self.model.id == id)
        # result = (await self.session.execute(stml)).scalar_one()
        
        result = await self.session.get(self.model, id)
        return result
    
    async def create(self, schema: BaseModel):
        '''Method creates object in DB'''

        new_obj = self.model(**schema.dict())
        self.session.add(new_obj)
        return new_obj
    
    async def update(self, email: str, schema: BaseModel):
        '''Method updates object in DB'''

        stml = update(self.model).where(self.model.email == email).values(**schema.dict(exclude_none=True)).returning(self.model)
        result = (await self.session.execute(stml)).scalar_one()
        return result
    
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from pydantic import BaseModel

from . repositories import ABCRepository


class SQLAchemyReposytory(ABCRepository):

    model: DeclarativeBase

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get(self, id: int):
        stml = select(self.model).where(self.model.id == id)
        result = (await self.session.execute(stml)).scalar_one()
        return result
    
    async def create(self, schema: BaseModel):
        new_obj = self.model(**schema.dict())
        self.session.add(new_obj)
        return new_obj
    
    async def update(self, email: str, schema: BaseModel):
        stml = update(self.model).where(self.model.email == email).values(**schema.dict(exclude_none=True)).returning(self.model)
        result = (await self.session.execute(stml)).scalar_one()
        return result
    
    
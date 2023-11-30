from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

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
        stml = insert(self.model).values(**schema.dict()).returning(self.model)
        res = await self.session.execute(stml)
        return res.scalar_one()
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import User
from src.settings import pwd_context


class UserManagerMixinRefreshTokens:
    
    async def refresh_tokens(self, refresh_token: str, email: str, session: AsyncSession):
        user = ...


class UserManagerProtectedMethods:

    async def _get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        stml = select(User).where(User.email == email)
        result = await session.execute(stml)
        result = result.scalar()
        return result
    
    def _verify_password(self, user: User) -> bool:
        return pwd_context.verify(self.data.password, user.hashed_password)
    
    def _create_access_token(self):
        access_token = self.access_security.create_access_token(subject={
            'username': self.data.username
        })
        return access_token
    
    def _create_refresh_token(self):
        refresh_token = self.refresh_security.create_refresh_token(subject={
            'username': self.data.username
        })
        return refresh_token
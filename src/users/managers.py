from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from fastapi import status

from pydantic import EmailStr

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.settings import access_security, refresh_security
from src.utils.managers import UserManagerABC

from . import mixins


class UserManager(
    mixins.UserManagerMixinAuthenticate,
    mixins.UserManagerMixinRefreshTokens,
    mixins.UserManagerMixinProtectedMethods,
    UserManagerABC
    ):

    def __init__(self, data: Optional[OAuth2PasswordRequestForm] = None):
        self.data: OAuth2PasswordRequestForm = data
        self.access_security = access_security
        self.refresh_security = refresh_security

    async def authanticate(self, session: AsyncSession):
        return await super().authanticate(session)
    
    async def refresh_tokens(self, refresh_token: str, email: EmailStr, session: AsyncSession):
        return await super().refresh_tokens(refresh_token, email, session)
    
    async def get_user_by_email(self, email: EmailStr, session: AsyncSession) -> User | None:
        return await super()._get_user_by_email(email, session)
    
    async def get_user_by_id(self, id: int, session: AsyncSession) -> User | None:
        return await super()._get_user_by_id(id, session)
    
    async def deactivate_user(self, email: EmailStr, session: AsyncSession):
        user = await self.get_user_by_email(email=email, session=session)
        user.is_active = False
        return user
    
    #TODO
    async def grant_admin_privilegios(self, email: EmailStr, user_email: EmailStr, session: AsyncSession):
        current_user = await self.get_user_by_email(email=email, session=session)
        if current_user.is_super_user:
            user = await self.get_user_by_email(email=user_email, session=session)
            user.role = user.grant_admin_privilegios()
            return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
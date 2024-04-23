#User manages

from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

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
    '''Class UserManager control user actions'''

    def __init__(self, data: Optional[OAuth2PasswordRequestForm] = None):
        '''Constructor'''

        self.data: Optional[OAuth2PasswordRequestForm] = data
        self.access_security = access_security
        self.refresh_security = refresh_security

    async def authanticate(self, session: AsyncSession):
        '''Method respons of authorization user'''
        
        return await super().authanticate(session) # type: ignore
    
    async def refresh_tokens(self, refresh_token: str, email: EmailStr, session: AsyncSession):
        '''Method response of refresh (update) tokens'''
        
        return await super().refresh_tokens(refresh_token, email, session)
    
    async def get_user_by_email(self, email: EmailStr, session: AsyncSession) -> User:
        '''Method returns user from DB'''
        
        return await super()._get_user_by_email(email, session)
    
    async def get_user_by_id(self, id: int, session: AsyncSession) -> User | None:
        '''Method returns user from DB'''
        
        return await super()._get_user_by_id(id, session)
    
    async def deactivate_user(self, email: EmailStr, session: AsyncSession):
        '''Method delete user, set status false in column is_active in DB'''

        user = await self.get_user_by_email(email=email, session=session)
        user.is_active = False
        return user
    
    async def grant_admin_privilegios(self, email: EmailStr, user_email: EmailStr, session: AsyncSession):
        '''Method add role admin to user'''

        return await super()._grant_admin_privilegios(email, user_email, session)
    
    async def revoke_admin_privilegios(self, email: EmailStr, user_email: EmailStr, session: AsyncSession):
        '''Method delete role admin from user'''

        return await super()._revoke_admin_privilegios(email, user_email, session)
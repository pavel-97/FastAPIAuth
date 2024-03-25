#Mixins

from typing import Optional

from fastapi import HTTPException, status

from pydantic import EmailStr

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from src.models import User
from src.settings import pwd_context


class UserManagerMixinAuthenticate:
    '''Class mixin adds method authorization'''

    async def authanticate(self, session: AsyncSession) -> dict:
        '''Method authorizates user'''

        user = await self._get_user_by_email(email=self.data.username, session=session)
        
        if user is None or not self._verify_password(user=user):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email (username) or password')
                
        refresh_token: str = self._create_refresh_token()
        user.refresh_token = refresh_token
        
        return {
            'access_token': self._create_access_token(),
            'refresh_token': refresh_token,
            'type_token': 'Bearer'
            }


class UserManagerMixinRefreshTokens:
    '''Class mixin adds method refresh (update) tokens'''

    async def refresh_tokens(self, refresh_token: str, email: EmailStr, session: AsyncSession) -> dict:
        '''Method refreshs (updates) access and refresh tokens'''

        user = await self._get_user_by_email(email=email, session=session)
        
        if user is None or user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token')
        
        access_token, refresh_token = self.create_access_refresh_tokens(data={'username': email})
        user.refresh_token = refresh_token

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'type_token': 'Bearer'
            }
    
    def create_access_refresh_tokens(self, data: dict) -> tuple[str]:
        '''Method return access and refresh tokens'''

        access_token: str = self.access_security.create_access_token(subject=data)
        refresh_token: str = self.refresh_security.create_refresh_token(subject=data)
        return access_token, refresh_token
    

class UserManagerMixinProtectedMethods:
    '''Class mixin adds protected methods'''

    async def _get_user_by_email(self, email: EmailStr, session: AsyncSession) -> Optional[User]:
        '''Protected method to get user by email'''

        stml = select(User).where(and_(User.email == email, User.is_active == True))
        result = (await session.execute(stml)).scalar()
        return result
    
    #TO DO
    async def _get_user_by_id(self, id: int, session: AsyncSession) -> Optional[User]:
        '''Protected method to get user by id'''

        stml = select(User).where(and_(User.id == id, User.is_active == True))
        result = (await session.execute(stml)).scalar()
        return result
    
    def _verify_password(self, user: User) -> bool:
        '''Protected method to check password'''

        return pwd_context.verify(self.data.password, user.hashed_password)
    
    def _create_access_token(self):
        '''Protected method to create access token'''

        access_token = self.access_security.create_access_token(subject={
            'username': self.data.username
        })
        return access_token
    
    def _create_refresh_token(self):
        '''Protected method to create refresh tokens'''

        refresh_token = self.refresh_security.create_refresh_token(subject={
            'username': self.data.username
        })
        return refresh_token
    
    async def _grant_admin_privilegios(self, email: EmailStr, user_email: EmailStr, session: AsyncSession):
        '''Protected method to grant admin privilegios for some user'''

        current_user = await self._get_user_by_email(email=email, session=session)
        if current_user.is_super_user:
            user = await self._get_user_by_email(email=user_email, session=session)
            user.role = user.grant_admin_privilegios()
            return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    async def _revoke_admin_privilegios(self, email: EmailStr, user_email: EmailStr, session: AsyncSession):
        '''Protected method to revoke admin privilegios from some user'''

        current_user = await self._get_user_by_email(email=email, session=session)
        if current_user.is_super_user:
            user = await self._get_user_by_email(email=user_email, session=session)
            user.role = user.revoke_admin_privilegios()
            return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
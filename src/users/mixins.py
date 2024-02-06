from typing import Optional

from fastapi import HTTPException, status

from pydantic import EmailStr

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from src.models import User
from src.settings import pwd_context


class UserManagerMixinAuthenticate:

    async def authanticate(self, session: AsyncSession):
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
    
    async def refresh_tokens(self, refresh_token: str, email: EmailStr, session: AsyncSession):
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
    
    def create_access_refresh_tokens(self, data: dict):
        access_token: str = self.access_security.create_access_token(subject=data)
        refresh_token: str = self.refresh_security.create_refresh_token(subject=data)
        return access_token, refresh_token
    

class UserManagerMixinProtectedMethods:

    async def _get_user_by_email(self, email: EmailStr, session: AsyncSession) -> Optional[User]:
        stml = select(User).where(and_(User.email == email, User.is_active == True))
        # print(5*'--*--', stml.compile(compile_kwargs={'literal_binds': True}))
        result = (await session.execute(stml)).scalar()
        return result
    
    async def _get_user_by_id(self, id: int, session: AsyncSession) -> Optional[User]:
        stml = select(User).where(and_(User.id == id, User.is_active == True))
        result = (await session.execute(stml)).scalar()
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
    
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import access_security, refresh_security

from .mixins import UserManagerProtectedMethods


#TODO
class UserManager(UserManagerProtectedMethods):

    def __init__(self, data: Optional[OAuth2PasswordRequestForm] = None):
        self.data: OAuth2PasswordRequestForm = data
        self.access_security = access_security
        self.refresh_security = refresh_security

    async def authanticate(self, session: AsyncSession):
        user = await self._get_user_by_email(email=self.data.username, session=session)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email (username) or password')
        
        if not self._verify_password(user=user):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email (username) or password'
            )
        
        refresh_token: str = self._create_refresh_token()
        user.refresh_token = refresh_token
        
        return {
            'access_token': self._create_access_token(),
            'refresh_token': refresh_token,
            'type_token': 'Bearer'
            }
    
    #TODO
    async def refresh_tokens(self, refresh_token: str, email: str, session: AsyncSession):
        user = await self._get_user_by_email(email=email, session=session)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email (username) or password')
        
        if user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token',
            )
        
        refresh_token = self.access_security.create_access_token(subject={'username': email})
        user.refresh_token = refresh_token

        return {
            'access_token': refresh_token,
            'refresh_token': self.refresh_security.create_refresh_token(subject={'username': email}),
            'type_token': 'Bearer'
            }
        

    # async def _get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
    #     stml = select(User).where(User.email == email)
    #     result = await session.execute(stml)
    #     result = result.scalar()
    #     return result
    
    # def _verify_password(self, user: User) -> bool:
    #     return pwd_context.verify(self.data.password, user.hashed_password)
    
    # def _create_access_token(self):
    #     access_token = self.access_security.create_access_token(subject={
    #         'username': self.data.username
    #     })
    #     return access_token
    
    # def _create_refresh_token(self):
    #     refresh_token = self.refresh_security.create_refresh_token(subject={
    #         'username': self.data.username
    #     })
    #     return refresh_token

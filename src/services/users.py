#User services

from fastapi.security import OAuth2PasswordRequestForm

from src.settings import get_password_hash
from src.schemas import RegistryUserDB
from src.schemas import AuthUserResponse, RefreshTokensResponse
from src.schemas import UpdateUser
from src.utils.unitofworks import AsyncUnitOfWork, UnitOfWork
from src.repositories.users import AsyncUserRepository, UserRepository
from src.managers.users import UserManager
from src.models import User


class UserService:
    '''Class User Service contains methods for views'''
    
    def registry(self, uow: UnitOfWork, registry_user: dict):
        '''Method registries user in DB'''
        
        with uow:
            hashed_password: str = get_password_hash(registry_user.pop('password'))
            registry_user = RegistryUserDB(hashed_password=hashed_password, **registry_user)
            result = UserRepository(session=uow.session).create(schema=registry_user)
            uow.commit()
        return result.read_model()
    
    async def update_user(self, uow: AsyncUnitOfWork, email: str, update_user: UpdateUser):
        '''Method updates user data in DB'''

        async with uow:
            user: User = await AsyncUserRepository(session=uow.session).update(email=email, schema=update_user)
            await uow.commit()
        return user.read_model()
    
    async def authenticate(self, uow: AsyncUnitOfWork, form_data: OAuth2PasswordRequestForm):
        '''Method authorizates user in app'''

        async with uow:
            result: dict = await UserManager(data=form_data).authanticate(session=uow.session)
            await uow.commit()
        return AuthUserResponse(**result)
        
    async def get_user_by_email(self, uow: AsyncUnitOfWork, email: str):
        '''Method returns user from DB by email'''

        async with uow:
            user = (await UserManager().get_user_by_email(email=email, session=uow.session)).read_model()
        return user

    async def refresh_tokens(self, uow: AsyncUnitOfWork, email: str, refresh_token: str):
        '''Method refreshs, updates access and refresh tokens'''

        async with uow:
            refresh_tokens: dict = await UserManager().refresh_tokens(
                    email=email,
                    refresh_token=refresh_token,
                    session=uow.session
                )
            await uow.commit()
        return RefreshTokensResponse(**refresh_tokens)
    
    async def delete_user(self, uow: AsyncUnitOfWork, email: str):
        '''Method sets field is_active false for some user in DB'''

        async with uow:
            user = (await UserManager().deactivate_user(email=email, session=uow.session)).read_model()
        return user
    
    async def grant_admin_privilegios(self, uow: AsyncUnitOfWork, email: str, user_email: str):
        '''Method grants admin privilegios for some user in DB'''

        async with uow:
            user = await UserManager().grant_admin_privilegios(email=email, user_email=user_email, session=uow.session)
            await uow.commit()
        return user
    
    async def revoke_admin_privilegios(self, uow: AsyncUnitOfWork, email: str, user_email: str):
        '''Method revokes admin privilegios for some user in DB'''

        async with uow:
            user = await UserManager().revoke_admin_privilegios(email=email, user_email=user_email, session=uow.session)
            await uow.commit()
        return user
    
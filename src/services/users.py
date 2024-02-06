from fastapi.security import OAuth2PasswordRequestForm

from src.settings import get_password_hash
from src.schemas import RegistryUserDB
from src.schemas import AuthUserResponse, RefreshTokensResponse
from src.schemas import UpdateUser
from src.utils.unitofworks import UnitOfWork
from src.repositories.users import UserRepository
from src.users.managers import UserManager
from src.models import User


class UserService:
    
    async def registry(self, uow: UnitOfWork, registry_user: dict):
        async with uow:
            hashed_password: str = get_password_hash(registry_user.pop('password'))
            registry_user = RegistryUserDB(hashed_password=hashed_password, **registry_user)
            result = await UserRepository(session=uow.session).create(schema=registry_user)
            await uow.commit()
        return result.read_model()
    
    async def update_user(self, uow: UnitOfWork, email: str, update_user: UpdateUser):
        async with uow:
            user: User = await UserRepository(session=uow.session).update(email=email, schema=update_user)
            await uow.commit()
        return user.read_model()
    
    async def authenticate(self, uow: UnitOfWork, form_data: OAuth2PasswordRequestForm):
        async with uow:
            result: dict = await UserManager(data=form_data).authanticate(session=uow.session)
            await uow.commit()
        return AuthUserResponse(**result)
        
    async def get_user_by_email(self, uow: UnitOfWork, email: str):
        async with uow:
            user = (await UserManager().get_user_by_email(email=email, session=uow.session)).read_model()
        return user

    async def refresh_tokens(self, uow: UnitOfWork, email: str, refresh_token: str):
        async with uow:
            refresh_tokens: dict = await UserManager().refresh_tokens(
                    email=email,
                    refresh_token=refresh_token,
                    session=uow.session
                )
            await uow.commit()
        return RefreshTokensResponse(**refresh_tokens)
    
    async def delete_user(self, uow: UnitOfWork, email: str):
        async with uow:
            user = (await UserManager().deactivate_user(email=email, session=uow.session)).read_model()
        return user
    
    #TODO
    async def grant_admin_privilegios(self, uow: UnitOfWork, email: str, user_email: str):
        async with uow:
            user = await UserManager().grant_admin_privilegios(email=email, user_email=user_email, session=uow.session)
            await uow.commit()
        return user


            
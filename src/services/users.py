from fastapi.security import OAuth2PasswordRequestForm

from src.settings import get_password_hash
from src.schemas import RegistryUser, RegistryUser2
from src.utils.unitofworks import UnitOfWork
from src.repositories.users import UserRepository
from src.users.managers import UserManager


class UserService:

    async def registry(self, uow: UnitOfWork, registry_user: RegistryUser):
        async with uow:
            hashed_password: str = get_password_hash(registry_user.dict().pop('password'))
            registry_user = RegistryUser2(hashed_password=hashed_password, **registry_user.dict())
            result = await UserRepository(session=uow.session).create(schema=registry_user)
            await uow.commit()
        return result
    
    async def authenticate(self, uow: UnitOfWork, form_data: OAuth2PasswordRequestForm):
        async with uow:
            user = await UserManager(data=form_data).authanticate(session=uow.session)
            await uow.commit()
        return user
        
    async def get_user_by_email(self, uow: UnitOfWork, email: str):
        async with uow:
            email = await UserManager()._get_user_by_email(email=email, session=uow.session)
        return email   

    async def refresh_tokens(self, uow: UnitOfWork, email: str, refresh_token: str):
        async with uow:
            refresh_tokens = await UserManager().refresh_tokens(email=email, refresh_token=refresh_token, session=uow.session)
            await uow.commit()
        return refresh_tokens

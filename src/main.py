from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Integer

from src.services.users import UserService

from . import dependencies
from . import schemas
from . import settings
from . import models
from . import admin


app = FastAPI()


@app.post('/login', response_model=schemas.AuthUserResponse)
async def authenticate_user(form_data: dependencies.OAuth2Dep, uow: dependencies.UOWDep):
    access_refresh_tokens: dict = await UserService().authenticate(uow=uow, form_data=form_data)
    return schemas.AuthUserResponse(**access_refresh_tokens)


@app.post('/registry')
async def registry(registry_user: schemas.RegistryUser, uow: dependencies.UOWDep):
    res = await UserService().registry(uow=uow, registry_user=registry_user)
    return res


#TODO
@app.post('/refresh', response_model=schemas.RefreshTokensResponse)
async def refresh_tokens(refresh_token: str, credentials: dependencies.JWTAuthCredentialsRefresh, uow: dependencies.UOWDep):
    email: str = credentials.subject.get('username')
    res = await UserService().refresh_tokens(uow=uow, email=email, refresh_token=refresh_token)
    return schemas.RefreshTokensResponse(**res)


@app.get('/token_protected')
async def token_protected(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep):
    email: str = credentials.subject.get('username')
    if email is not None:
        await UserService().get_user_by_email(uow=uow, email=email)
    return {'payload': credentials}


#TO DO
@app.get('/users')
async def get_all_users(q = Depends(token_protected), session: AsyncSession = Depends(settings.get_async_session)):
    async with session:
        stml = select(
            cast(func.avg(models.User.id), Integer).label('avg')
            )
        res = await session.execute(stml)
        res = res.scalars().all()
    return {'users': res}


admin.admin.mount_to(app)

from fastapi import FastAPI, Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Integer, desc
from sqlalchemy.orm import aliased

from src.services.users import UserService

from . import dependencies
from . import schemas
from . import settings
from . import models
from . import admin

from . import tasks


app = FastAPI()


@app.post('/login', response_model=schemas.AuthUserResponse)
async def authenticate_user(form_data: dependencies.OAuth2Dep, uow: dependencies.UOWDep):
    result = await UserService().authenticate(uow=uow, form_data=form_data)
    return result


@app.post('/registry')
async def registry(registry_user: schemas.RegistryUser):
    tasks.registry_task.delay(data=registry_user.dict())
    return {'status': status.HTTP_200_OK}


@app.post('/refresh', response_model=schemas.RefreshTokensResponse)
async def refresh_tokens(refresh_token: str, credentials: dependencies.JWTAuthCredentialsRefresh, uow: dependencies.UOWDep):
    email: str = credentials.subject.get('username')
    result = await UserService().refresh_tokens(uow=uow, email=email, refresh_token=refresh_token)
    return result


@app.get('/profile', response_model=schemas.User)
async def token_protected(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep):
    email: str = credentials.subject.get('username')
    user = await UserService().get_user_by_email(uow=uow, email=email)
    return user


@app.patch('/profile', response_model=schemas.User)
async def update_profile(update_user: schemas.UpdateUser, credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep):
    result = await UserService().update_user(
        uow=uow, 
        email=credentials.subject.get('username'),
        update_user=update_user
        )
    return result


@app.delete('/profile', response_model=schemas.User)
async def delete_user(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep):
    result = await UserService().delete_user(
        uow=uow,
        email=credentials.subject.get('username')
    )
    return result


#TODO
@app.patch('/grant_admin_privilegios')
async def grant_admin_privilegios(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep, user_email: str):
    result = await UserService().grant_admin_privilegios(
        uow=uow, 
        email=credentials.subject.get('username'),
        user_email=user_email
        )
    return result


#TODO
@app.get('/users')
async def get_all_users(session: AsyncSession = Depends(settings.get_async_session)):
    # async with session:
    #     stml = select(
    #         cast(func.avg(models.User.id), Integer).label('avg')
    #         )
    #     res = await session.execute(stml)
    #     res = res.scalars().all()

    async with session:
        u = aliased(models.User)
        subq = (
            select(
                u.id,
                u.email,
                u.create_at,
                func.avg(u.id).over(partition_by=u.id).label('n')
            )
        )
        cte = (
            select(
                subq.c.id,
                subq.c.email,
                subq.c.n
            ).cte('user2')
        )
        query = select(cte).order_by(desc(cte.c.n))
        res = await session.execute(query)
    # res = res.scalars()
    response = [(i.id, i.email, i.n) for i in res]
    # print(res[0])
    # return {'users': res}
    return {'result': response}

admin.admin.mount_to(app)

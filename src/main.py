#Views

from fastapi import FastAPI
from fastapi import status

from pydantic import EmailStr

from src.services.users import UserService

from . import dependencies
from . import schemas
from . import admin
from . tasks import registry_task


app = FastAPI()


@app.post('/registry')
def registry(registry_user: schemas.RegistryUser):
    '''Registration user'''
    
    registry_task.delay(registry_user.dict())
    return status.HTTP_200_OK


@app.post('/login', response_model=schemas.AuthUserResponse)
async def authenticate_user(form_data: dependencies.OAuth2Dep, uow: dependencies.UOWDep):
    '''Authorization for microservices'''

    result = await UserService().authenticate(uow=uow, form_data=form_data)
    return result


@app.post('/refresh', response_model=schemas.RefreshTokensResponse)
async def refresh_tokens(refresh_token: str, credentials: dependencies.JWTAuthCredentialsRefresh, uow: dependencies.UOWDep):
    '''Get refresh token to update access token'''
    
    email: EmailStr = credentials.subject.get('username')
    result = await UserService().refresh_tokens(uow=uow, email=email, refresh_token=refresh_token)
    return result


@app.get('/profile', response_model=schemas.User)
async def token_protected(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep):
    '''Get data current user'''
    
    email: EmailStr = credentials.subject.get('username')
    user = await UserService().get_user_by_email(uow=uow, email=email)
    return user


@app.patch('/profile', response_model=schemas.User)
async def update_profile(update_user: schemas.UpdateUser, credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep):
    '''Update data current user'''
    
    result = await UserService().update_user(
        uow=uow, 
        email=credentials.subject.get('username'),
        update_user=update_user
        )
    return result


@app.delete('/profile', response_model=schemas.User)
async def delete_user(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep):
    '''Delete current user'''
    
    result = await UserService().delete_user(
        uow=uow,
        email=credentials.subject.get('username')
    )
    return result


@app.patch('/grant_admin_privilegios')
async def grant_admin_privilegios(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep, user_email: EmailStr):
    '''Grant admin privilegios for user'''
    
    result = await UserService().grant_admin_privilegios(
        uow=uow, 
        email=credentials.subject.get('username'),
        user_email=user_email
        )
    return result


@app.patch('/revoke_admin_privilegios')
async def revoke_admin_privilegios(credentials: dependencies.JWTAuthCredentials, uow: dependencies.UOWDep, user_email: EmailStr):
    '''Revoke admin privilegios for user'''
    
    result = await UserService().revoke_admin_privilegios(
        uow=uow,
        email=credentials.subject.get('username'),
        user_email=user_email
    )
    return result


admin.admin.mount_to(app)

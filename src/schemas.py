#Pydantic models, schemas

import enum

from pydantic import BaseModel, EmailStr


class Role(str, enum.Enum):
    '''Role for user schema'''
    
    super_user = 'super_user'
    admin = 'admin'
    user = 'user'


class User(BaseModel):
    '''User schema'''
    
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: list[Role]


class AuthUser(BaseModel):
    '''Schema for input authorization data'''
    
    email: str
    password: str


class AuthUserResponse(BaseModel):
    '''Schema for response after authorization'''
    
    access_token: str
    refresh_token: str
    type_token: str


class RefreshTokensResponse(BaseModel):
    '''Schema for update tokens'''
    
    access_token: str
    refresh_token: str
    type_token: str
    

class RegistryUser(BaseModel):
    '''Schema for registration user'''

    email: str
    password: str
    first_name: str | None
    last_name: str | None


class RegistryUserDB(BaseModel):
    '''Schema for save data in DB'''

    email: str
    hashed_password: str
    first_name: str | None
    last_name: str | None
    role: list[Role] = [Role.user, ]


class UpdateUser(BaseModel):
    '''Schema for update user'''

    email: str | None
    first_name: str | None
    last_name: str | None
import enum

from pydantic import BaseModel, EmailStr



class Role(str, enum.Enum):
    super_user = 'super_user'
    admin = 'admin'
    user = 'user'


class User(BaseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: list[Role]


class AuthUser(BaseModel):
    email: str
    password: str


class AuthUserResponse(BaseModel):
    access_token: str
    refresh_token: str
    type_token: str


class RefreshTokensResponse(BaseModel):
    access_token: str
    refresh_token: str
    type_token: str
    

class RegistryUser(BaseModel):
    email: str
    password: str
    first_name: str | None
    last_name: str | None


class RegistryUserDB(BaseModel):
    email: str
    hashed_password: str
    first_name: str | None
    last_name: str | None
    role: list[Role] = [Role.user, ]


class UpdateUser(BaseModel):
    email: str | None
    first_name: str | None
    last_name: str | None
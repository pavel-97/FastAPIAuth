from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_jwt import JwtAuthorizationCredentials

from src.utils.unitofworks import UnitOfWork

from . import settings


UOWDep = Annotated[UnitOfWork, Depends()]
OAuth2Dep = Annotated[OAuth2PasswordRequestForm, Depends()]
JWTAuthCredentials = Annotated[JwtAuthorizationCredentials, Security(settings.access_security)]
JWTAuthCredentialsRefresh = Annotated[JwtAuthorizationCredentials, Security(settings.refresh_security)]
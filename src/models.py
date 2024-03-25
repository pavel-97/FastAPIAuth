#Models

import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, String
from sqlalchemy.dialects.postgresql import ARRAY

from .settings import Base
from . import schemas


class Role(str, enum.Enum):
    '''Roles for User model'''
    
    super_user = 'super_user'
    admin = 'admin'
    user = 'user'


class User(Base):
    '''Table user'''
    
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[list[Role]] = mapped_column(ARRAY(String))
    hashed_password: Mapped[str]
    refresh_token: Mapped[str | None]
    create_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    update_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow)
    
    def read_model(self):
        '''Convert user object to pydantic object'''
        
        return schemas.User(**self.__dict__)
    
    @property
    def is_super_user(self) -> bool:
        '''Check role'''
        
        return Role.super_user in self.role

    @property
    def is_admin(self) -> bool:
        '''Check role'''
        
        return Role.admin in self.role
    
    def grant_admin_privilegios(self):
        '''Add role admin to user'''
        
        if Role.admin not in self.role:
            return {*self.role, Role.admin}
        return {*self.role}
    
    def revoke_admin_privilegios(self):
        '''Delete role admin from user'''

        if Role.admin in self.role:
            self.role.remove(Role.admin)
        return {*self.role}
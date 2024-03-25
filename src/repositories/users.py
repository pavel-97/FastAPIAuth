#User repository

from src.utils.sql_alchemy_repositories import AsyncSQLAlchemyReposytory
from src.utils.sql_alchemy_repositories import SQLAlchemyReposytory
from src.models import User


class UserRepository(SQLAlchemyReposytory):
    '''Class User Repository works with DB (create, update data)'''

    model = User


class AsyncUserRepository(AsyncSQLAlchemyReposytory):
    '''Class Async User Repository works with DB (create, update data)'''
    
    model = User

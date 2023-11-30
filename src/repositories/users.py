from src.utils.sql_alchemy_repositories import SQLAchemyReposytory
from src.models import User



class UserRepository(SQLAchemyReposytory):
    
    model = User

    
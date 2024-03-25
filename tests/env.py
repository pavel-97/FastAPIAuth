#Env

from typing import Final

from environs import Env


env = Env()
env.read_env()

POSTGRES_USER_TEST: Final = env.str('POSTGRES_USER_TEST')
POSTGRES_PASSWORD_TEST: Final = env.str('POSTGRES_PASSWORD_TEST')
POSTGRES_DB_TEST: Final = env.str('POSTGRES_DB_TEST')

SECRET_KEY: Final = env.str('SECRET_KEY')
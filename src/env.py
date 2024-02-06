from typing import Final

from environs import Env


env = Env()
env.read_env()

POSTGRES_USER: Final = env.str('POSTGRES_USER')
POSTGRES_PASSWORD: Final = env.str('POSTGRES_PASSWORD')
POSTGRES_DB: Final = env.str('POSTGRES_DB')

SECRET_KEY: Final = env.str('SECRET_KEY')

RABBITMQ_DEFAULT_USER: Final = env.str('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS: Final = env.str('RABBITMQ_DEFAULT_PASS')

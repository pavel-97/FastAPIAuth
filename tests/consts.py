#Constants

from src.models import Role


SUPER_USER_DATA: dict = {
    'email': 'test_super_user@mail.com',
    'password': 'test_pwd',
    'role': [Role.super_user]
}


USER_DATA: dict = {
    'email': 'test_user_2@mail.com',
    'password': 'test_pwd',
    'role': [Role.user],
}

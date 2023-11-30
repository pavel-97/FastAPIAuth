from starlette_admin.contrib.sqla import ModelView
from starlette_admin import action

from fastapi import Request

from .settings import admin
from .models import User


class UserAdmin(ModelView):
    actions = ['act1', ]

    @action(name='act1', text='make act1')
    async def act1(self, request: Request, objs: list):
        return objs


admin.add_view(UserAdmin(User))

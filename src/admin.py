#Admin panel, settings admin panel

from starlette_admin.contrib.sqla import ModelView
from starlette_admin import action

from fastapi import Request

from .settings import admin
from .models import User


class UserAdmin(ModelView):
    '''Settings admin panel for some model'''
    
    actions = ['act1', ]

    @action(name='act1', text='make act1')
    async def act1(self, request: Request, objs: list):
        '''Make somethins with selected objects'''
        return objs


admin.add_view(UserAdmin(User))

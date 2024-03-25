#Test revoke privilegios

import pytest

from httpx import AsyncClient

from tests.utils import TestAccessUser

from src.models import Role


class TestRevokeAdminPrivilegios(TestAccessUser):
    '''Class test revoke admin privilegios'''
    
    async def test_prevent_revoke_admin_privilegios(self, async_client: AsyncClient):
        '''Authorized client dont revoke admin privilegios'''

        response_token = await self.test_auth(async_client)
        token = response_token.json().get('access_token')
        response = await async_client.patch(
            '/grant_admin_privilegios',
            headers={'Authorization': f'Bearer {token}'},
            params={
                'user_email': 'test_user_2@mail.com'
            }
        )
        assert response.status_code == 403

    @pytest.mark.usefixtures('create_super_user')
    async def test_revoke_admin_privilegios(self, async_client: AsyncClient):
        '''Super user revoke admin privilegios'''

        response_token = await async_client.post('/login', data={
            'username': 'test_super_user@mail.com',
            'password': 'test_pwd'
        })
        token = response_token.json().get('access_token')
        
        response_grant = await async_client.patch(
            '/grant_admin_privilegios',
            headers={'Authorization': f'Bearer {token}'},
            params={
                'user_email': 'test_user_2@mail.com'
            }
            )

        response = await async_client.patch(
            '/revoke_admin_privilegios',
            headers={'Authorization': f'Bearer {token}'},
            params={
                'user_email': 'test_user_2@mail.com'
            }
        )

        assert response_grant.status_code == 200
        assert response.status_code == 200
        assert Role.admin not in response.json().get('role')
        
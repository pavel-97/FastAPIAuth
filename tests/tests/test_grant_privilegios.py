import pytest

from httpx import AsyncClient

from tests.utils import TestAccessUser


class TestGrantPrivilegios(TestAccessUser):

    async def test_prevent_grant_privilegios(self, async_client: AsyncClient):
        response_token = await self.test_auth(async_client)
        token = response_token.json().get('access_token')
        response = await async_client.patch(
            '/grant_admin_privilegios', 
            headers={'Authorization': f'Bearer {token}'},
            params={
                'user_email': 'test_user_2@mail.com'
                })
        assert response.status_code == 403

    @pytest.mark.usefixtures('create_super_user')
    async def test_grant_privilegios(self, async_client: AsyncClient):
        response_token = await async_client.post('/login', data={
            'username': 'test_super_user@mail.com',
            'password': 'test_pwd'
        })
        token = response_token.json().get('access_token')
        response = await async_client.patch(
            '/grant_admin_privilegios',
            headers={'Authorization': f'Bearer {token}'},
            params={
                'user_email': 'test_user_2@mail.com'
            }
            )
        assert response.status_code == 200
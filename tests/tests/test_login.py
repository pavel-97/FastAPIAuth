import pytest

from httpx import AsyncClient


class TestAuthenticateUser:
    
    @pytest.mark.usefixtures('registry')
    async def test_auth(self, async_client: AsyncClient):
        response = await async_client.post('/login', data={
            'username': 'test_user_2@mail.com',
            'password': 'test_pwd',
        })
        assert response.status_code == 200
        return response


class TestAuthenticateUserByWorngEmailPassword:

    async def test_auth_by_wrong_email(self, async_client: AsyncClient):
        response = await async_client.post('/login', data={
            'username': 'test_wrong_user@mail.com',
            'password': 'test_pwd',
        })
        assert response.status_code == 401


    async def test_auth_by_wrong_password(self, async_client: AsyncClient):
        response = await async_client.post('/login', data={
            'username': 'test_user@mail.com',
            'password': 'test_wrong_pwd',
        })
        assert response.status_code == 401
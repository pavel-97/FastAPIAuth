#Test utils

import pytest

from httpx import AsyncClient


class TestAccessUser:
    
    @pytest.mark.usefixtures('registry')
    async def test_auth(self, async_client: AsyncClient):
        response = await async_client.post('/login', data={
            'username': 'test_user_2@mail.com',
            'password': 'test_pwd',
        })
        assert response.status_code == 200
        return response

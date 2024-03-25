#Test deactivate user

from httpx import AsyncClient

from ..utils import TestAccessUser


class TestDeactivateUser(TestAccessUser):
    '''Class test deactivate user'''

    async def test_deactivate_user(self, async_client: AsyncClient):
        '''Auzorized client deletes own profile'''

        response_token = await self.test_auth(async_client)
        token: str = response_token.json().get('access_token')

        response = await async_client.delete('/profile', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200

    async def test_deactivate_user_unauth(self, async_client: AsyncClient):
        '''Client dont delete own profile'''
        
        response = await async_client.delete('/profile')
        assert response.status_code == 401

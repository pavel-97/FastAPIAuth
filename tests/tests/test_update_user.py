from httpx import AsyncClient

from ..utils import TestAccessUser


class TestUpdateUser(TestAccessUser):

    async def test_update_user(self, async_client: AsyncClient):
        response_token = await self.test_auth(async_client)
        token: str = response_token.json().get('access_token')
        
        response = await async_client.patch('/profile', 
                                            headers={'Authorization': f'Bearer {token}' }, 
                                            json={
                                                'first_name': 'test_name_1', 
                                                'last_name': 'test_name_2',
                                                })
        assert response.status_code == 200

    async def test_update_user_unauth(self, async_client: AsyncClient):
        response = await async_client.patch('/profile',  
                                            json={
                                                'first_name': 'test_name_1', 
                                                'last_name': 'test_name_2',
                                                })
        assert response.status_code == 401
    
    async def test_update_user_by_wrong_data(self, async_client: AsyncClient):
        response_token = await self.test_auth(async_client)
        token: str = response_token.json().get('access_token')
        
        response = await async_client.patch('/profile', 
                                            headers={'Authorization': f'Bearer {token}' }, 
                                            json={
                                                'first_name': 'null', 
                                                'last_name': 'test_name_3',
                                                'wrong_key': 'some_data'
                                                })
        assert response.status_code == 200
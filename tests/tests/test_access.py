#Test access

from sqlalchemy import select

from httpx import AsyncClient

from src.models import User

from ..conftest import async_engine_test
from ..utils import TestAccessUser


class TestAccessUserByToken(TestAccessUser):
    '''Class test access user by tokens'''

    async def test_get_all_users(self, async_client: AsyncClient):
        '''Authorized client gets all users'''

        response_toke = await self.test_auth(async_client)
        token = response_toke.json().get('access_token')
        response = await async_client.get('/users', headers={'Authorization': f'Bearer {token}' })
        assert response.status_code == 200


    async def test_token_protected(self, async_client: AsyncClient):
        '''Client makes authorization'''

        response_token = await self.test_auth(async_client)
        token: str = response_token.json().get('access_token')
        response = await async_client.get('/profile', headers={'Authorization': f'Bearer {token}' })
        assert response.status_code == 200


    async def test_refresh_tokens(self, async_client: AsyncClient):
        '''Authorizaed client refresh (update) tokens with valid refresh token'''

        response_token = await self.test_auth(async_client)
        refresh_token: str = response_token.json().get('refresh_token')
        
        response = await async_client.post('/refresh',
                                        params={
                                            'refresh_token': refresh_token
                                            },
                                        headers={
                                            'Authorization': f'Bearer {refresh_token}'
                                            })
        assert response.status_code == 200

    async def test_refresh_token_in_db(self, async_client: AsyncClient):
        '''Compare client refresh token with refresh token saved in DB'''

        response_token = await self.test_auth(async_client)
        refresh_token: str = response_token.json().get('refresh_token')

        async with async_engine_test.connect() as conn:
            stml = select(User).where(User.email == 'test_user_2@mail.com')
            res = await conn.execute(stml)
        result = res.all()[0]
        assert result.refresh_token == refresh_token


class TestAccessUserByWrongToken(TestAccessUser):
    '''Class test access user by wrong tokens'''

    async def test_token_protected_by_wrong_token(self, async_client: AsyncClient):
        '''Clent dont get access with unvalid access token'''

        response_token = await self.test_auth(async_client)
        token: str = response_token.json().get('access_token')
        response = await async_client.get('/profile', headers={'Authorization': f'Bearer {token}asdasqwdasd' })
        assert response.status_code == 401
import pytest

from sqlalchemy.exc import IntegrityError

from httpx import AsyncClient


data: dict = {
    'email': 'test_user@mail.com',
    'password': 'test_pwd',
    'role': ["user", ],
}


@pytest.mark.parametrize('user_data', [data])
class TestRegistryUserUnique:
    ...
    # async def test_registry(self, async_client: AsyncClient, user_data: dict):
    #     response = await async_client.post('/registry', json=user_data)
    #     assert response.status_code == 200

    # async def test_model_user_unique_email(self, async_client: AsyncClient, user_data: dict):
    #     with pytest.raises(IntegrityError):
    #         await async_client.post('/registry', json=user_data)


class TestRegistryUserWrongRole:

    async def test_model_user_wrong_role(self, async_client: AsyncClient):
        response = await async_client.post('/registry', json={
            'email': 'test_user@mail.com',
            'password': 'test_pwd',
            'role': ["usr", ],
        })
        assert response.status_code == 422

import pytest

from sqlalchemy.exc import IntegrityError

from httpx import AsyncClient


data: dict = {
    'email': 'test_user@mail.com',
    'password': 'test_pwd',
    'role': ["user", ],
}


@pytest.mark.parametrize('data', [data])
async def test_registry(async_client: AsyncClient, data: dict):
    response = await async_client.post('/registry', json=data)
    assert response.status_code == 200


@pytest.mark.parametrize('data', [data])
async def test_model_user_unique_email(async_client: AsyncClient, data: dict):
    with pytest.raises(IntegrityError):
        await async_client.post('/registry', json=data)


async def test_model_user_role(async_client: AsyncClient):
    response = await async_client.post('/registry', json={
        'email': 'test_user@mail.com',
        'password': 'test_pwd',
        'role': ["usr", ],
    })
    assert response.status_code == 422


async def test_get_all_users(async_client: AsyncClient):
    response_toke = await test_auth(async_client)
    token = response_toke.json().get('access_token')
    response = await async_client.get('/users', headers={'Authorization': f'Bearer {token}' })
    assert response.status_code == 200


async def test_auth(async_client: AsyncClient):
    response = await async_client.post('/login', data={
        'username': 'test_user@mail.com',
        'password': 'test_pwd',
    })
    assert response.status_code == 200
    return response


async def test_auth_by_wrong_email(async_client: AsyncClient):
    response = await async_client.post('/login', data={
        'username': 'test_wrong_user@mail.com',
        'password': 'test_pwd',
    })
    assert response.status_code == 401


async def test_auth_by_wrong_password(async_client: AsyncClient):
    response = await async_client.post('/login', data={
        'username': 'test_user@mail.com',
        'password': 'test_wrong_pwd',
    })
    assert response.status_code == 401


async def test_token_protected(async_client: AsyncClient):
    response_token = await test_auth(async_client)
    token: str = response_token.json().get('access_token')
    response = await async_client.get('/token_protected', headers={'Authorization': f'Bearer {token}' })
    assert response.status_code == 200


async def test_token_protected_by_wrong_token(async_client: AsyncClient):
    response_token = await test_auth(async_client)
    token: str = response_token.json().get('access_token')
    response = await async_client.get('/token_protected', headers={'Authorization': f'Bearer {token}asdasqwdasd' })
    assert response.status_code == 401


async def test_refresh_tokens(async_client: AsyncClient):
    response_token = await test_auth(async_client)
    refresh_token: str = response_token.json().get('refresh_token')
    
    response = await async_client.post('/refresh',
                                       params={
                                           'refresh_token': refresh_token
                                           },
                                       headers={
                                           'Authorization': f'Bearer {refresh_token}'
                                           })
    assert response.status_code == 200


# async def test_refresh_token_in_db(async_client:AsyncClient):

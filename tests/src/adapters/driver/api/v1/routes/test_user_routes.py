import pytest
from fastapi import status
from datetime import datetime

from src.constants.permissions import UserPermissions
from src.core.exceptions.utils import ErrorCode
from tests.factories.user_factory import UserFactory


@pytest.mark.parametrize(
    'payload', [
        {'name': 'user1', 'password': 'pass1pass'},
        {'name': 'user2', 'password': 'pass2pass'},
    ]
)
def test_create_user_success(client, payload):
    response = client.post('/api/v1/users', json=payload, permissions=[UserPermissions.CAN_CREATE_USER])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['name'] == payload['name']


def test_create_user_duplicate_name_return_error(client):
    payload = {'name': 'user1', 'password': 'pass1pass'}

    response = client.post('/api/v1/users', json=payload, permissions=[UserPermissions.CAN_CREATE_USER])
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post('/api/v1/users', json=payload, permissions=[UserPermissions.CAN_CREATE_USER])
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'User already exists.',
            'details': None
        }
    }


def test_reactivate_permission_return_success(client):
    user = UserFactory(inactivated_at=datetime.now())

    payload = {'name': user.name, 'password': 'pass1pass'}
    response = client.post('/api/v1/users', json=payload, permissions=[UserPermissions.CAN_CREATE_USER])

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    
    data = response.json()
    assert 'id' in data


def test_create_user_send_unexpected_param_return_error(client):
    payload = {'name': 'user1', 'password': 'pass1pass', 'fubar': 'fubar'}

    response = client.post('/api/v1/users', json=payload, permissions=[UserPermissions.CAN_CREATE_USER])

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_name_greater_than_limit_return_error(client):
    payload = {'name': 'user1'*25, 'password': 'pass1pass'}
    response = client.post('/api/v1/users', json=payload, permissions=[UserPermissions.CAN_CREATE_USER])

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_user_by_name_return_success(client):
    user = UserFactory()
    response = client.get(f'/api/v1/users/{user.name}/name', permissions=[UserPermissions.CAN_VIEW_USERS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == user.id
    assert data['name'] == user.name


def test_get_user_by_id_return_success(client):
    user = UserFactory()
    response = client.get(f'/api/v1/users/{user.id}/id', permissions=[UserPermissions.CAN_VIEW_USERS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == user.id
    assert data['name'] == user.name


def test_get_all_users_return_success(client):
    user1 = UserFactory()
    user2 = UserFactory()

    response = client.get('/api/v1/users', permissions=[UserPermissions.CAN_VIEW_USERS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {'id': user1.id, 'name': user1.name},
        {'id': user2.id, 'name': user2.name}
    ]


def test_update_user_return_success(client):
    user = UserFactory()
    payload = {'id': user.id, 'name': 'new_name', 'password': 'new_pass'}

    response = client.put(f'/api/v1/users/{user.id}', json=payload, permissions=[UserPermissions.CAN_UPDATE_USER])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': user.id, 'name': 'new_name'}


def test_delete_user_return_success(client):
    user1 = UserFactory()
    user2 = UserFactory()

    response = client.delete(f'/api/v1/users/{user1.id}', permissions=[UserPermissions.CAN_DELETE_USER])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/users', permissions=[UserPermissions.CAN_VIEW_USERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [{'id': user2.id, 'name': user2.name}]
    
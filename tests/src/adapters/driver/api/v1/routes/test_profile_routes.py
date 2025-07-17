from datetime import datetime
import pytest
from fastapi import status

from src.constants.permissions import ProfilePermissions
from src.core.exceptions.utils import ErrorCode
from tests.factories.profile_factory import ProfileFactory


@pytest.mark.parametrize('payload', [
    {'name': 'Manager', 'description': 'Store Manager'},
    {'name': 'Assistant', 'description': 'Store Worker'}
])
def test_create_profile_success(client, payload):
    response = client.post('/api/v1/profiles', json=payload, permissions=[ProfilePermissions.CAN_CREATE_PROFILE]) 

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert 'id' in data
    assert data['name'] == payload['name']
    assert data['description'] == payload['description']



def test_create_profile_duplicate_name_and_return_error(client):
    payload = {'name': 'Manager', 'description': 'Store Manager'}
    response = client.post('/api/v1/profiles', json=payload, permissions=[ProfilePermissions.CAN_CREATE_PROFILE])
    
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post('/api/v1/profiles', json=payload, permissions=[ProfilePermissions.CAN_CREATE_PROFILE])

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Profile already exists.',
            'details': None,
        }
    }


def test_reactivate_profile_and_return_success(client):
    ProfileFactory(name='Manager', description='Store Manager', inactivated_at=datetime.now())

    payload = {'name': 'Manager', 'description': 'Store Manager'}
    response = client.post('/api/v1/profiles', json=payload, permissions=[ProfilePermissions.CAN_CREATE_PROFILE])

    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()

    assert 'id' in response_json
    assert response_json['name'] == payload['name']
    assert response_json['description'] == payload['description']


def test_send_unexpected_param_to_create_profile_and_return_error(client):
    payload = {'name': 'Manager', 'description': 'Store Manager', 'unexpected': '123'}
    response = client.post('/api/v1/profiles', json=payload, permissions=[ProfilePermissions.CAN_CREATE_PROFILE])

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_p_name_greater_than_limit_and_return_error(client):
    payload = {'name': 'ManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManagerManager',
                'description': 'Store Manager'}
    
    response = client.post('/api/v1/profiles', json=payload, permissions=[ProfilePermissions.CAN_CREATE_PROFILE])

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_profile_by_name_and_return_success(client):
    ProfileFactory(name='Manager', description='Store Manager')
    ProfileFactory(name='Assistant', description='Store Worker')

    response = client.get('/api/v1/profiles/Manager/name', permissions=[ProfilePermissions.CAN_VIEW_PROFILES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': 1, 'name': 'Manager', 'description': 'Store Manager'}


def test_get_profile_by_id_and_return_success(client):
    ProfileFactory(name='Manager', description='Store Manager')
    ProfileFactory(name='Assistant', description='Store Worker')

    response = client.get('/api/v1/profiles/1/id', permissions=[ProfilePermissions.CAN_VIEW_PROFILES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': 1, 'name': 'Manager', 'description': 'Store Manager'}


def test_get_all_profiles_and_return_success(client):
    ProfileFactory(name='Manager', description='Store Manager')
    ProfileFactory(name='Assistant', description='Store Worker')

    response = client.get('/api/v1/profiles', permissions=[ProfilePermissions.CAN_VIEW_PROFILES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {'id': 1, 'name': 'Manager', 'description': 'Store Manager'},
        {'id': 2, 'name': 'Assistant', 'description': 'Store Worker'}
    ]


def test_update_profile_and_return_success(client):
    ProfileFactory(name='Manager', description='Store Manager')
    ProfileFactory(name='Assistant', description='Store Worker')

    payload = {'id': 1, 'name': 'Manager - Updated', 'description': 'Store Manager - Updated'}

    response = client.put('/api/v1/profiles/1', json=payload, permissions=[ProfilePermissions.CAN_UPDATE_PROFILE])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': 1, 'name': 'Manager - Updated', 'description': 'Store Manager - Updated'}


def test_delete_profile_and_return_success(client):
    ProfileFactory(name='Manager', description='Store Manager')
    ProfileFactory(name='Assistant', description='Store Worker')

    response = client.delete('/api/v1/profiles/2', permissions=[ProfilePermissions.CAN_DELETE_PROFILE])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/profiles', permissions=[ProfilePermissions.CAN_VIEW_PROFILES])
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == [{'id': 1, 'name': 'Manager', 'description': 'Store Manager'}]


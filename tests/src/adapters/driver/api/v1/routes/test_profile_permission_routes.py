from datetime import datetime
from src.constants.permissions import ProfilePermissionPermissions
from src.core.exceptions.utils import ErrorCode
from tests.factories.profile_permission_factory import ProfilePermissionFactory
from tests.factories.permission_factory import PermissionFactory
from tests.factories.profile_factory import ProfileFactory

from fastapi import status


def test_create_profile_permission(client, db_session):
    permission = PermissionFactory()
    profile = ProfileFactory()
    payload = {'permission_id': permission.id, 'profile_id': profile.id}
    
    response = client.post('api/v1/profile_permissions', json=payload, permissions=[ProfilePermissionPermissions.CAN_CREATE_PROFILE_PERMISSION])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert 'id' in data
    assert data['permission']['id'] == permission.id
    assert data['profile']['id'] == profile.id


def test_create_duplicate_profile_permission_and_return_error(client, db_session):
    profile_permission = ProfilePermissionFactory()
    payload = {'permission_id': profile_permission.permission_id, 'profile_id': profile_permission.profile_id}
    
    response = client.post('api/v1/profile_permissions', json=payload, permissions=[ProfilePermissionPermissions.CAN_CREATE_PROFILE_PERMISSION])

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Profile Permission already exists.',
            'details': None,
        }
    }

def test_reactivate_profile_permission_and_return_success(client, db_session):
    profile_permission = ProfilePermissionFactory(inactivated_at=datetime.now())
    payload = {'permission_id': profile_permission.permission_id, 'profile_id': profile_permission.profile_id}

    response = client.post('api/v1/profile_permissions', json=payload, permissions=[ProfilePermissionPermissions.CAN_CREATE_PROFILE_PERMISSION])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert 'id' in data
    assert data['permission']['id'] == profile_permission.permission_id
    assert data['profile']['id'] == profile_permission.profile_id


def test_get_profile_permission_by_id_and_return_sucess(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get(f'/api/v1/profile_permissions/{profile_permission_2.id}/id', permissions=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'id' in data
    assert data['id'] == profile_permission_2.id
    assert data['permission']['id'] == profile_permission_2.permission_id
    assert data['profile']['id'] == profile_permission_2.profile_id


def test_get_profile_permission_by_permission_id_and_return_success(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get(f'/api/v1/profile_permissions/{profile_permission_2.permission_id}/permission_id', permissions=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'id' in data
    assert data['permission']['id'] == profile_permission_2.permission_id
    assert data['profile']['id'] == profile_permission_2.profile_id

def test_get_profile_permission_by_profile_id_and_return_success(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get(f'/api/v1/profile_permissions/{profile_permission_2.profile_id}/profile_id', permissions=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'id' in data
    assert data['permission']['id'] == profile_permission_2.permission_id
    assert data['profile']['id'] == profile_permission_2.profile_id


def test_get_all_profile_permissions_return_success(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get('/api/v1/profile_permissions', permissions=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            'id': profile_permission_1.id,
            'permission': {
                'id': profile_permission_1.permission.id,
                'name': profile_permission_1.permission.name,
                'description': profile_permission_1.permission.description
            },
            'profile': {
                'id': profile_permission_1.profile.id,
                'name': profile_permission_1.profile.name,
                'description': profile_permission_1.profile.description
            }
        },
        {
            'id': profile_permission_2.id,
            'permission': {
                'id': profile_permission_2.permission.id,
                'name': profile_permission_2.permission.name,
                'description': profile_permission_2.permission.description
            },
            'profile': {
                'id': profile_permission_2.profile.id,
                'name': profile_permission_2.profile.name,
                'description': profile_permission_2.profile.description
            }
        }
    ]


def test_update_profile_permission_and_return_success(client):
    permission = PermissionFactory()
    profile_permission = ProfilePermissionFactory()

    payload = [{
        'id': profile_permission.id,
        'permission': {
            'id': permission.id,
            'name': permission.name,
            'description': permission.description
        },
        'profile': {
            'id': profile_permission.profile.id,
            'name': profile_permission.profile.name,
            'description': profile_permission.profile.description
        }
    }]

    payload = {
        'id': profile_permission.id,
        'permission_id': permission.id,
        'profile_id': profile_permission.profile.id
    }
    
    response = client.put(f'/api/v1/profile_permissions/{profile_permission.id}', json=payload, permissions=[ProfilePermissionPermissions.CAN_UPDATE_PROFILE_PERMISSION])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        'id': profile_permission.id,
        'permission': {
            'id': permission.id,
            'name': permission.name,
            'description': permission.description
        },
        'profile': {
            'id': profile_permission.profile.id,
            'name': profile_permission.profile.name,
            'description': profile_permission.profile.description
        }
    }


def test_delete_profile_permission_and_return_success(client):
    profile_permission1 = ProfilePermissionFactory()
    profile_permission2 = ProfilePermissionFactory()

    response = client.delete(f'api/v1/profile_permissions/{profile_permission1.id}', permissions=[ProfilePermissionPermissions.CAN_DELETE_PROFILE_PERMISSION])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/profile_permissions', permissions=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data == [{
        'id': profile_permission2.id,
        'permission': {
            'id': profile_permission2.permission.id,
            'name': profile_permission2.permission.name,
            'description': profile_permission2.permission.description
        },
        'profile': {
            'id': profile_permission2.profile.id,
            'name': profile_permission2.profile.name,
            'description': profile_permission2.profile.description
        }
    }]
    

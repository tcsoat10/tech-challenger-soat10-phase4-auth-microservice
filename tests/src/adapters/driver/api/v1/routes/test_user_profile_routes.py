from datetime import datetime
from fastapi import status

from src.constants.permissions import UserProfilePermissions
from src.core.exceptions.utils import ErrorCode
from tests.factories.profile_factory import ProfileFactory
from tests.factories.user_factory import UserFactory
from tests.factories.user_profile_factory import UserProfileFactory


def test_create_user_profile_success(client):
    user = UserFactory()
    profile = ProfileFactory()

    response = client.post('/api/v1/user-profiles', json={'user_id': user.id, 'profile_id': profile.id}, permissions=[UserProfilePermissions.CAN_CREATE_USER_PROFILE])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data['user']['id'] == user.id
    assert data['profile']['id'] == profile.id

def test_create_user_profile_with_unregistered_user_id_and_return_error(client):
    profile = ProfileFactory()

    response = client.post('/api/v1/user-profiles', json={'user_id': 999, 'profile_id': profile.id}, permissions=[UserProfilePermissions.CAN_CREATE_USER_PROFILE])
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'User not found.',
            'details': None,
        }
    }

def test_reactivate_user_profile_success(client):
    user_profile = UserProfileFactory(inactivated_at=datetime.now())

    response = client.post('/api/v1/user-profiles', json={'user_id': user_profile.user_id, 'profile_id': user_profile.profile_id}, permissions=[UserProfilePermissions.CAN_CREATE_USER_PROFILE])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data['id'] == user_profile.id
    assert data['user']['id'] == user_profile.user_id
    assert data['profile']['id'] == user_profile.profile_id


def test_create_user_profile_with_unregistered_profile_id_and_return_error(client):
    user = UserFactory()

    response = client.post('/api/v1/user-profiles', json={'user_id': user.id, 'profile_id': 999}, permissions=[UserProfilePermissions.CAN_CREATE_USER_PROFILE])
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Profile not found.',
            'details': None,
        }
    }

def test_create_user_profile_with_unregistered_user_id_and_profile_id_and_return_error(client):
    response = client.post('/api/v1/user-profiles', json={'user_id': 999, 'profile_id': 999}, permissions=[UserProfilePermissions.CAN_CREATE_USER_PROFILE])
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'User not found.',
            'details': None,
        }
    }

def test_get_user_profile_by_id_success(client):
    user_profile = UserProfileFactory()

    response = client.get(f'/api/v1/user-profiles/{user_profile.id}', permissions=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == user_profile.id
    assert data['user']['id'] == user_profile.user_id
    assert data['profile']['id'] == user_profile.profile_id

def test_get_user_profile_by_id_with_unregistered_id_and_return_error(client):
    response = client.get('/api/v1/user-profiles/999', permissions=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'UserProfile not found.',
            'details': None,
        }
    }

def test_get_user_profile_by_user_id_and_profile_id_success(client):
    UserProfileFactory()

    response = client.get('/api/v1/user-profiles/1/1', permissions=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['user']['id'] == 1
    assert data['profile']['id'] == 1

def test_get_user_profile_by_user_id_and_profile_id_with_unregistered_ids_and_return_error(client):
    response = client.get('/api/v1/user-profiles/999/999', permissions=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'UserProfile not found.',
            'details': None,
        }
    }

def test_get_all_user_profiles_success(client):
    UserProfileFactory.create_batch(3)

    response = client.get('/api/v1/user-profiles', permissions=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 3

def test_get_all_user_profiles_with_deleted(client):
    UserProfileFactory.create_batch(3, inactivated_at=datetime.now())

    response = client.get('/api/v1/user-profiles?include_deleted=true', permissions=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 3

def test_update_user_profile_success(client):
    user_profile = UserProfileFactory()

    response = client.put(
        f'/api/v1/user-profiles/{user_profile.id}',
        json={'id': user_profile.id, 'user_id': user_profile.user_id, 'profile_id': user_profile.profile_id},
        permissions=[UserProfilePermissions.CAN_UPDATE_USER_PROFILE]
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == user_profile.id
    assert data['user']['id'] == user_profile.user_id
    assert data['profile']['id'] == user_profile.profile_id

def test_update_user_profile_with_unregistered_user_id_and_return_error(client):
    user_profile = UserProfileFactory()

    response = client.put(
        f'/api/v1/user-profiles/{user_profile.id}',
        json={'id': user_profile.id, 'user_id': 999, 'profile_id': user_profile.profile_id},
        permissions=[UserProfilePermissions.CAN_UPDATE_USER_PROFILE]
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'User not found.',
            'details': None,
        }
    }

def test_update_user_profile_with_unregistered_profile_id_and_return_error(client):
    user_profile = UserProfileFactory()

    response = client.put(
        f'/api/v1/user-profiles/{user_profile.id}',
        json={'id': user_profile.id, 'user_id': user_profile.user_id, 'profile_id': 999},
        permissions=[UserProfilePermissions.CAN_UPDATE_USER_PROFILE]
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data =={
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Profile not found.',
            'details': None,
        }
    }

def test_delete_user_profile_success(client):
    user_profile = UserProfileFactory()

    response = client.delete(f'/api/v1/user-profiles/{user_profile.id}', permissions=[UserProfilePermissions.CAN_DELETE_USER_PROFILE])
    assert response.status_code == status.HTTP_204_NO_CONTENT

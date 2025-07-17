from datetime import datetime
import pytest
from fastapi import status

from src.constants.permissions import PermissionPermissions
from src.core.exceptions.utils import ErrorCode
from tests.factories.permission_factory import PermissionFactory


@pytest.mark.parametrize('payload', [
    {'name': 'Admin', 'description': 'System Admin privileges'},
    {'name': 'Employee', 'description': 'System user privileges'}
])
def test_create_permission_success(client, payload):
    response = client.post('/api/v1/permissions', json=payload, permissions=[PermissionPermissions.CAN_CREATE_PERMISSION]) 

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert 'id' in data
    assert data['name'] == payload['name']
    assert data['description'] == payload['description']



def test_create_permission_duplicate_name_and_return_error(client):
    payload = {'name': 'Admin', 'description': 'System Admin privileges'}
    response = client.post('/api/v1/permissions', json=payload, permissions=[PermissionPermissions.CAN_CREATE_PERMISSION])
    
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post('/api/v1/permissions', json=payload, permissions=[PermissionPermissions.CAN_CREATE_PERMISSION])

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Permission already exists.',
            'details': None,
        }
    }


def test_reactivate_permission_and_return_success(client):
    PermissionFactory(name='Admin', description='System Admin privileges', inactivated_at=datetime.now())

    payload = {'name': 'Admin', 'description': 'System Admin privileges'}
    response = client.post('/api/v1/permissions', json=payload, permissions=[PermissionPermissions.CAN_CREATE_PERMISSION])

    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()

    assert 'id' in response_json
    assert response_json['name'] == payload['name']
    assert response_json['description'] == payload['description']


def test_send_unexpected_param_to_create_permission_and_return_error(client):
    payload = {'name': 'Admin', 'description': 'System Admin privileges', 'unexpected': '123'}
    response = client.post('/api/v1/permissions', json=payload, permissions=[PermissionPermissions.CAN_CREATE_PERMISSION])

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_permission_name_greater_than_limit_and_return_error(client):
    payload = {'name': 'AdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdminAdmin',
                'description': 'System Admin privileges'}
    
    response = client.post('/api/v1/permissions', json=payload, permissions=[PermissionPermissions.CAN_CREATE_PERMISSION])

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_permission_by_name_and_return_success(client):
    PermissionFactory(name='Admin', description='System Admin privileges')
    PermissionFactory(name='Employee', description='System user privileges')

    response = client.get('/api/v1/permissions/Admin/name', permissions=[PermissionPermissions.CAN_VIEW_PERMISSIONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': 1, 'name': 'Admin', 'description': 'System Admin privileges'}


def test_get_permission_by_id_and_return_success(client):
    PermissionFactory(name='Admin', description='System Admin privileges')
    PermissionFactory(name='Employee', description='System user privileges')

    response = client.get('/api/v1/permissions/1/id', permissions=[PermissionPermissions.CAN_VIEW_PERMISSIONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': 1, 'name': 'Admin', 'description': 'System Admin privileges'}


def test_get_all_permissions_and_return_success(client):
    PermissionFactory(name='Admin', description='System Admin privileges')
    PermissionFactory(name='Employee', description='System user privileges')

    response = client.get('/api/v1/permissions', permissions=[PermissionPermissions.CAN_VIEW_PERMISSIONS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {'id': 1, 'name': 'Admin', 'description': 'System Admin privileges'},
        {'id': 2, 'name': 'Employee', 'description': 'System user privileges'}
    ]


def test_update_permission_and_return_success(client):
    PermissionFactory(name='Admin', description='System Admin privileges')
    PermissionFactory(name='Employee', description='System user privileges')

    payload = {'id': 1, 'name': 'Admin - Updated', 'description': 'System Admin privileges - Updated'}

    response = client.put('/api/v1/permissions/1', json=payload, permissions=[PermissionPermissions.CAN_UPDATE_PERMISSION])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': 1, 'name': 'Admin - Updated', 'description': 'System Admin privileges - Updated'}


def test_delete_permission_and_return_success(client):
    PermissionFactory(name='Admin', description='System Admin privileges')
    PermissionFactory(name='Employee', description='System user privileges')

    response = client.delete('/api/v1/permissions/2', permissions=[PermissionPermissions.CAN_DELETE_PERMISSION])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/permissions', permissions=[PermissionPermissions.CAN_VIEW_PERMISSIONS])
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == [{'id': 1, 'name': 'Admin', 'description': 'System Admin privileges'}]


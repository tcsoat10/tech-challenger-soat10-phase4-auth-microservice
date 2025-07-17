from datetime import datetime
import pytest
from fastapi import status

from src.constants.permissions import RolePermissions
from src.core.exceptions.utils import ErrorCode
from tests.factories.role_factory import RoleFactory


@pytest.mark.parametrize(
    'payload', [
        {'name': 'Role1', 'description': 'Desc1'},
        {'name': 'Role2', 'description': 'Desc2'}
    ]
)
def test_create_role_success(client, payload):
    response = client.post('/api/v1/roles', json=payload, permissions=[RolePermissions.CAN_CREATE_ROLE])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert 'id' in data
    assert data['name'] == payload['name']
    assert data['description'] == payload['description']


def test_create_duplicated_role_and_return_error(client):
    payload = {'name': 'Role1', 'description': 'Desc1'}
    response = client.post('/api/v1/roles', json=payload, permissions=[RolePermissions.CAN_CREATE_ROLE])

    assert response.status_code == status.HTTP_201_CREATED

    response = client.post('/api/v1/roles', json=payload, permissions=[RolePermissions.CAN_CREATE_ROLE])

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Role already exists.',
            'details': None,
        }
    }


def test_reactivate_role_and_return_success(client):
    RoleFactory(name='Role1', description='Desc1', inactivated_at=datetime.now())

    payload = {'name': 'Role1', 'description': 'Desc1'}
    response = client.post('/api/v1/roles', json=payload, permissions=[RolePermissions.CAN_CREATE_ROLE])

    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()

    assert 'id' in response_json
    assert response_json['name'] == payload['name']
    assert response_json['description'] == payload['description']


def test_create_role_name_greater_than_limit_and_return_error(client):
    payload = {'name': 'Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1Role1', 
               'description': 'Desc1'}
    response = client.post('/api/v1/roles', json=payload, permissions=[RolePermissions.CAN_CREATE_ROLE])

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_role_by_name_and_return_success(client):
    role = RoleFactory()

    response = client.get(f'/api/v1/roles/{role.name}/name', permissions=[RolePermissions.CAN_VIEW_ROLES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': role.id, 'name': role.name, 'description': role.description}


def test_get_role_by_id_and_return_success(client):
    role = RoleFactory()

    response = client.get(f'/api/v1/roles/{role.id}/id', permissions=[RolePermissions.CAN_VIEW_ROLES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': role.id, 'name': role.name, 'description': role.description}


def test_get_all_roles_and_return_success(client):
    role1 = RoleFactory()
    role2 = RoleFactory()

    response = client.get('/api/v1/roles', permissions=[RolePermissions.CAN_VIEW_ROLES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == [
        {'id': role1.id, 'name': role1.name, 'description': role1.description},
        {'id': role2.id, 'name': role2.name, 'description': role2.description}
    ]


def test_update_role_and_return_success(client):
    role = RoleFactory()

    response = client.put(f'/api/v1/roles/{role.id}', json={'id': role.id, 'name': role.name, 'description': 'Updated description'}, permissions=[RolePermissions.CAN_UPDATE_ROLE])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {'id': role.id, 'name': role.name, 'description': 'Updated description'}


def test_delete_role_and_return_success(client):
    role1 = RoleFactory()
    role2 = RoleFactory()

    response = client.delete(f'/api/v1/roles/{role2.id}', permissions=[RolePermissions.CAN_DELETE_ROLE])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/roles', permissions=[RolePermissions.CAN_VIEW_ROLES])
    data = response.json()
    assert data == [{'id': role1.id, 'name': role1.name, 'description': role1.description}]

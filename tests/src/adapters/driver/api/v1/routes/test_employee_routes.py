from tests.factories.person_factory import PersonFactory
from tests.factories.role_factory import RoleFactory
from tests.factories.user_factory import UserFactory
from tests.factories.employee_factory import EmployeeFactory
from src.core.exceptions.utils import ErrorCode
from src.constants.permissions import EmployeePermissions
from pycpfcnpj import gen

from fastapi import status
from datetime import datetime
from tests.factories.customer_factory import CustomerFactory


def test_create_employee_success(client):
    role = RoleFactory()
    user = UserFactory()
    payload = {
        'role_id': role.id,
        'user_id': user.id,
        'person': {
            'name': 'John Doe',
            'cpf': gen.cpf(),
            'email': 'johndoe@example.com',
            'birth_date': '1990-01-01'
        }
    }
    
    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['person']['name'] == payload['person']['name']
    assert data['person']['cpf'] == payload['person']['cpf']
    assert data['person']['email'] == payload['person']['email']
    assert data['person']['birth_date'] == payload['person']['birth_date']
    assert data['role']['id'] == role.id
    assert data['user']['id'] == user.id


def test_create_duplicate_employee_return_error(client):
    employee = EmployeeFactory()
    payload = {
        'role_id': employee.role_id,
        'user_id': employee.user_id,
        'person': {
            'name': employee.person.name,
            'cpf': employee.person.cpf,
            'email': employee.person.email,
            'birth_date': employee.person.birth_date.strftime('%Y-%m-%d')
        }
    }

    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Employee already exists.',
            'details': None,
        }
    }


def test_reactivate_employee_success(client):
    employee = EmployeeFactory(inactivated_at=datetime.now())
    payload = {
        'role_id': employee.role_id,
        'user_id': employee.user_id,
        'person': {
            'name': employee.person.name,
            'cpf': employee.person.cpf,
            'email': employee.person.email,
            'birth_date': employee.person.birth_date.strftime('%Y-%m-%d')
        },
    }

    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['person']['id'] == employee.person_id
    assert data['role']['id'] == employee.role_id
    assert data['user']['id'] == employee.user_id

def test_create_employee_with_duplicate_email_return_error(client):
    existing_employee = EmployeeFactory()
    role = RoleFactory()
    user = UserFactory()
    payload = {
        'role_id': role.id,
        'user_id': user.id,
        'person': {
            'name': 'Different Name',
            'cpf': gen.cpf(),
            'email': existing_employee.person.email,  # Same email
            'birth_date': '1990-01-01'
        }
    }

    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail']['code'] == str(ErrorCode.DUPLICATED_ENTITY)


def test_create_employee_with_duplicate_cpf_return_error(client):
    existing_employee = EmployeeFactory()
    role = RoleFactory()
    user = UserFactory()
    payload = {
        'role_id': role.id,
        'user_id': user.id,
        'person': {
            'name': 'Different Name',
            'cpf': existing_employee.person.cpf,
            'email': 'different@email.com',
            'birth_date': '1990-01-01'
        }
    }

    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail']['code'] == str(ErrorCode.DUPLICATED_ENTITY)

def test_create_employee_with_duplicate_user_return_error(client):
    existing_employee = EmployeeFactory()
    role = RoleFactory()
    payload = {
        'role_id': role.id,
        'user_id': existing_employee.user_id,
        'person': {
            'name': 'John Doe',
            'cpf': gen.cpf(),
            'email': 'johndoe@example.com',
            'birth_date': '1990-01-01'
        }
    }

    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail']['code'] == str(ErrorCode.DUPLICATED_ENTITY)


def test_create_employee_with_duplicate_person_return_error(client):
    existing_employee = EmployeeFactory()
    role = RoleFactory()
    user = UserFactory()
    payload = {
        'role_id': role.id,
        'user_id': user.id,
        'person': {
            'name': existing_employee.person.name,
            'cpf': existing_employee.person.cpf,
            'email': existing_employee.person.email,
            'birth_date': existing_employee.person.birth_date.strftime('%Y-%m-%d')
        }
    }

    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail']['code'] == str(ErrorCode.DUPLICATED_ENTITY)

def test_create_employee_with_duplicate_username_return_error(client):
    existing_employee = EmployeeFactory()
    role = RoleFactory()
    payload = {
        'role_id': role.id,
        'user_id': existing_employee.user_id,  # Same user
        'person': {
            'name': 'Different Name',
            'cpf': gen.cpf(),
            'email': 'different@email.com',
            'birth_date': '1990-01-01'
        }
    }

    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail']['code'] == str(ErrorCode.DUPLICATED_ENTITY)


def test_update_inactive_employee_return_error(client):
    employee = EmployeeFactory(inactivated_at=datetime.now())
    person = PersonFactory()
    payload = {'id': employee.id, 'person_id': person.id, 'role_id': employee.role.id, 'user_id': employee.user.id}

    response = client.put(f'/api/v1/employees/{employee.id}', json=payload, permissions=[EmployeePermissions.CAN_UPDATE_EMPLOYEE])
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_employee_by_id_success(client):
    employee = EmployeeFactory()

    response = client.get(f'/api/v1/employees/{employee.id}/id', permissions=[EmployeePermissions.CAN_VIEW_EMPLOYEES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'id' in data
    assert data['person']['id'] == employee.person_id
    assert data['role']['id'] == employee.role_id
    assert data['user']['id'] == employee.user_id

def test_create_employee_with_person_linked_to_customer_success(client):
    customer = CustomerFactory()
    role = RoleFactory()
    user = UserFactory()

    payload = {
        'role_id': role.id,
        'user_id': user.id,
        'person': {
            'name': customer.person.name,
            'cpf': customer.person.cpf,
            'email': customer.person.email,
            'birth_date': customer.person.birth_date.strftime('%Y-%m-%d')
        }
    }
    
    response = client.post('/api/v1/employees', json=payload, permissions=[EmployeePermissions.CAN_CREATE_EMPLOYEE])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['person']['cpf'] == customer.person.cpf
    assert data['person']['email'] == customer.person.email

def test_get_employee_by_person_id_success(client):
    employee = EmployeeFactory()

    response = client.get(f'/api/v1/employees/{employee.person_id}/person_id', permissions=[EmployeePermissions.CAN_VIEW_EMPLOYEES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'id' in data
    assert data['person']['id'] == employee.person_id
    assert data['role']['id'] == employee.role_id
    assert data['user']['id'] == employee.user_id


def test_get_employee_by_user_id_success(client):
    employee = EmployeeFactory()

    response = client.get(f'/api/v1/employees/{employee.user_id}/user_id', permissions=[EmployeePermissions.CAN_VIEW_EMPLOYEES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'id' in data
    assert data['person']['id'] == employee.person_id
    assert data['role']['id'] == employee.role_id
    assert data['user']['id'] == employee.user_id


def test_get_employees_by_role_id_success(client):
    role = RoleFactory()
    employee1 = EmployeeFactory(role=role)
    employee2 = EmployeeFactory(role=role)
    employee3 = EmployeeFactory()

    response = client.get(f'/api/v1/employees/{role.id}/role_id', permissions=[EmployeePermissions.CAN_VIEW_EMPLOYEES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2
    assert data == [
        {
            'id': employee1.id,
            'person': {
                'id': employee1.person.id,
                'name': employee1.person.name,
                'cpf': employee1.person.cpf,
                'email': employee1.person.email,
                'birth_date': employee1.person.birth_date.strftime('%Y-%m-%d'),
            },
            'role': {
                'id': role.id,
                'name': role.name,
                'description': role.description
            },
            'user': {
                'id': employee1.user.id,
                'name': employee1.user.name
            }
        },
        {
            'id': employee2.id,
            'person': {
                'id': employee2.person.id,
                'name': employee2.person.name,
                'cpf': employee2.person.cpf,
                'email': employee2.person.email,
                'birth_date': employee2.person.birth_date.strftime('%Y-%m-%d'),
            },
            'role': {
                'id': role.id,
                'name': role.name,
                'description': role.description
            },
            'user': {
                'id': employee2.user.id,
                'name': employee2.user.name
            }
        }
    ]


def test_get_all_employees_success(client):
    employee1 = EmployeeFactory()
    employee2 = EmployeeFactory()

    response = client.get('/api/v1/employees', permissions=[EmployeePermissions.CAN_VIEW_EMPLOYEES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2
    assert data == [
        {
            'id': employee1.id,
            'person': {
                'id': employee1.person.id,
                'name': employee1.person.name,
                'cpf': employee1.person.cpf,
                'email': employee1.person.email,
                'birth_date': employee1.person.birth_date.strftime('%Y-%m-%d'),
            },
            'role': {
                'id': employee1.role.id,
                'name': employee1.role.name,
                'description': employee1.role.description
            },
            'user': {
                'id': employee1.user.id,
                'name': employee1.user.name
            }
        },
        {
            'id': employee2.id,
            'person': {
                'id': employee2.person.id,
                'name': employee2.person.name,
                'cpf': employee2.person.cpf,
                'email': employee2.person.email,
                'birth_date': employee2.person.birth_date.strftime('%Y-%m-%d'),
            },
            'role': {
                'id': employee2.role.id,
                'name': employee2.role.name,
                'description': employee2.role.description
            },
            'user': {
                'id': employee2.user.id,
                'name': employee2.user.name
            }
        }
    ]


def update_employee_success(client):
    person = PersonFactory()
    employee = EmployeeFactory()

    payload = {'id': employee.id, 'person_id': person.id, 'role_id': employee.role.id, 'user_id': employee.user.id}

    response = client.put(f'/api/v1/employees/{employee.id}', json=payload, permissions=[EmployeePermissions.CAN_UPDATE_EMPLOYEE])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        'id': employee.id,
            'person': {
                'id': person.id,
                'name': person.name,
                'cpf': person.cpf,
                'email': person.email,
                'birth_date': person.birth_date.strftime('%Y-%m-%d'),
            },
            'role': {
                'id': employee.role.id,
                'name': employee.role.name,
                'description': employee.role.description
            },
            'user': {
                'id': employee.user.id,
                'name': employee.user.name
            }
    }


def test_delete_employee_success(client):
    employee1 = EmployeeFactory()
    employee2 = EmployeeFactory()

    response = client.delete(f'/api/v1/employees/{employee1.id}', permissions=[EmployeePermissions.CAN_DELETE_EMPLOYEE])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/employees', permissions=[EmployeePermissions.CAN_VIEW_EMPLOYEES])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [{
        'id': employee2.id,
            'person': {
                'id': employee2.person.id,
                'name': employee2.person.name,
                'cpf': employee2.person.cpf,
                'email': employee2.person.email,
                'birth_date': employee2.person.birth_date.strftime('%Y-%m-%d'),
            },
            'role': {
                'id': employee2.role.id,
                'name': employee2.role.name,
                'description': employee2.role.description
            },
            'user': {
                'id': employee2.user.id,
                'name': employee2.user.name
            }
    }]
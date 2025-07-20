import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from datetime import datetime

from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO
from src.core.domain.entities.customer import Customer
from src.core.domain.entities.employee import Employee
from src.core.domain.entities.person import Person
from src.core.domain.entities.permission import Permission
from src.core.domain.entities.profile import Profile
from src.core.domain.entities.role import Role
from src.core.domain.entities.user import User
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.invalid_credentials_exception import InvalidCredentialsException
from tests.bdd.support.auth_helpers import AuthTestHelper

scenarios('../features/authentication.feature')

@pytest.fixture
def auth_helper(db_session):
    return AuthTestHelper(db_session)

@given('que o sistema está funcionando')
def system_is_running(db_session):
    assert db_session is not None

@given(parsers.parse('existe um perfil "{profile_name}" cadastrado'))
def simple_profile_registered(profile_name, auth_helper, context):
    existing_profile = auth_helper.get_profile_by_name(profile_name)
    if not existing_profile:
        profile = Profile(name=profile_name, description=f'Profile {profile_name}')
        created_profile = auth_helper.create_profile(profile)
        context['profile'] = created_profile
    else:
        context['profile'] = existing_profile

@given(parsers.parse('existe um perfil "{profile_name}" com as permissões:'))
def profile_with_multiple_permissions(profile_name, auth_helper, context, datatable):
    existing_profile = auth_helper.get_profile_by_name(profile_name)
    print(f"Buscando perfil '{profile_name}'...")
    
    if existing_profile:
        print(f"Perfil '{profile_name}' encontrado nas migrações com {len(existing_profile.permissions)} permissões")
        context['profile'] = existing_profile
    else:
        print(f"Perfil '{profile_name}' não encontrado, criando novo...")
        profile = Profile(name=profile_name, description=f'Perfil {profile_name}')
        created_profile = auth_helper.create_profile(profile)

        permissions = []
        for row in datatable:
            permission_name = row[0]
            existing_permission = auth_helper.get_permission_by_name(permission_name)
            if existing_permission:
                permissions.append(existing_permission)
            else:
                permission = Permission(name=permission_name, description=f'Permissão {permission_name}')
                created_permission = auth_helper.create_permission(permission)
                permissions.append(created_permission)

        auth_helper.associate_profile_with_permissions(created_profile, permissions)
        updated_profile = auth_helper.reload_profile_with_permissions(created_profile)
        context['profile'] = updated_profile

@given(parsers.parse('existe um perfil "{profile_name}" com a permissão "{permission_name}"'))
def profile_with_single_permission(profile_name, permission_name, auth_helper, context):
    profile = Profile(name=profile_name, description=f'Perfil {profile_name}')
    created_profile = auth_helper.create_profile(profile)
    
    permission = Permission(name=permission_name, description=f'Permissão {permission_name}')
    created_permission = auth_helper.create_permission(permission)

    auth_helper.associate_profile_with_permissions(created_profile, [created_permission])
    updated_profile = auth_helper.reload_profile_with_permissions(created_profile)
    context['profile'] = updated_profile

@given(parsers.parse('existe um cliente com CPF "{cpf}" cadastrado'))
def customer_registered(cpf, auth_helper, context):
    person = Person(
        name='João Silva', 
        cpf=cpf, 
        email=f'{cpf.replace(".", "").replace("-", "")}@example.com', 
        birth_date=datetime.now().date()
    )
    customer = Customer(person=person)
    created_customer = auth_helper.create_customer(customer)
    context['customer'] = created_customer

@given(parsers.parse('existe um funcionário com usuário "{username}" e senha "{password}"'))
def employee_registered(username, password, auth_helper, context):
    from pycpfcnpj import gen
    
    person = Person(
        name='Jane Doe', 
        cpf=gen.cpf(), 
        email='jane.doe@example.com', 
        birth_date=datetime.now().date()
    )
    user = User(name=username, password=password)
    role = Role(name='employee', description='Employee Role')
    
    created_role = auth_helper.create_role(role)
    employee = Employee(person=person, user=user, role=created_role)
    auth_helper.create_employee(employee)
    context['employee'] = employee

@given(parsers.parse('existe um gerente com usuário "{username}" e senha "{password}"'))
def manager_registered(username, password, auth_helper, context):
    from pycpfcnpj import gen
    
    person = Person(
        name='Manager User', 
        cpf=gen.cpf(), 
        email='manager@example.com', 
        birth_date=datetime.now().date()
    )
    user = User(name=username, password=password)
    role = Role(name='manager', description='Manager Role')
    
    created_role = auth_helper.create_role(role)
    employee = Employee(person=person, user=user, role=created_role)
    auth_helper.create_employee(employee)
    context['manager'] = employee

@when(parsers.parse('eu faço login com o CPF "{cpf}"'))
def login_with_cpf(cpf, auth_helper, context):
    try:
        dto = AuthByCpfDTO(cpf=cpf)
        result = auth_helper.login_by_cpf(dto)
        context['auth_result'] = result
        context['auth_error'] = None
    except Exception as e:
        context['auth_result'] = None
        context['auth_error'] = e

@when(parsers.parse('eu faço login com o CPF "{cpf}" que não está cadastrado'))
def login_with_unregistered_cpf(cpf, auth_helper, context):
    try:
        dto = AuthByCpfDTO(cpf=cpf)
        result = auth_helper.login_by_cpf(dto)
        context['auth_result'] = result
        context['auth_error'] = None
    except Exception as e:
        context['auth_result'] = None
        context['auth_error'] = e

@when(parsers.parse('eu faço login com usuário "{username}" e senha "{password}"'))
def login_with_employee_credentials(username, password, auth_helper, context):
    try:
        dto = LoginDTO(username=username, password=password)
        result = auth_helper.login_employee(dto)
        context['auth_result'] = result
        context['auth_error'] = None
    except Exception as e:
        context['auth_result'] = None
        context['auth_error'] = e

@when('eu faço um login anônimo')
def login_anonymous(auth_helper, context):
    try:
        result = auth_helper.login_anonymous()
        context['auth_result'] = result
        context['auth_error'] = None
    except Exception as e:
        context['auth_result'] = None
        context['auth_error'] = e

@then('eu devo receber um token de acesso')
def verify_access_token(context):
    assert 'auth_error' not in context or context['auth_error'] is None, f"Erro inesperado: {context.get('auth_error')}"
    assert context.get('auth_result') is not None
    assert 'access_token' in context['auth_result']
    assert context['auth_result']['access_token'] is not None

@then(parsers.parse('o token deve conter as informações do usuário com CPF "{cpf}"'))
def verify_user_info_cpf(cpf, auth_helper, context):
    token_payload = auth_helper.decode_token(context['auth_result']['access_token'])
    assert token_payload['person']['cpf'] == cpf

@then(parsers.parse('o token deve conter o perfil "{profile_name}"'))
def verify_profile_token(profile_name, auth_helper, context):
    token_payload = auth_helper.decode_token(context['auth_result']['access_token'])
    assert token_payload['profile']['name'] == profile_name

@then(parsers.parse('o token deve conter as permissões:'))
def verify_multiple_permissions_token(auth_helper, context, datatable):
    token_payload = auth_helper.decode_token(context['auth_result']['access_token'])
    token_permissions = token_payload['profile']['permissions']
    
    for row in datatable:
        permission_name = row[0]
        assert permission_name in token_permissions, \
            f"Permissão '{permission_name}' não encontrada no token. Permissões disponíveis: {token_permissions}"

@then(parsers.parse('eu devo receber um erro de "{error_type}"'))
def verify_auth_error(error_type, context):
    assert 'auth_error' in context and context['auth_error'] is not None, "Nenhum erro foi lançado quando deveria ter sido."
    error = context['auth_error']
    
    if error_type == "usuário não encontrado":
        assert isinstance(error, EntityNotFoundException)
    elif error_type == "credenciais inválidas":
        assert isinstance(error, InvalidCredentialsException)
    else:
        pytest.fail(f"Tipo de erro desconhecido: {error_type}")

from datetime import datetime
import pytest
from src.core.domain.entities.person import Person
from src.adapters.driver.api.v1.controllers.auth_controller import AuthController
from src.core.domain.entities.customer import Customer
from src.core.domain.entities.employee import Employee
from src.core.domain.entities.permission import Permission
from src.core.domain.entities.profile import Profile
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.invalid_credentials_exception import InvalidCredentialsException
from tests.factories.role_factory import RoleFactory

@pytest.fixture
def mock_customer_repository(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_profile_repository(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_employee_repository(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_auth_provider_gateway(mocker):
    return mocker.Mock()
    
@pytest.fixture
def auth_controller(
    mock_customer_repository,
    mock_profile_repository,
    mock_employee_repository,
    mock_auth_provider_gateway,
    db_session
):
    employee_gateway = mock_employee_repository
    customer_gateway = mock_customer_repository
    profile_gateway = mock_profile_repository
    auth_provider_gateway = mock_auth_provider_gateway
    
    controller = AuthController(profile_gateway, employee_gateway, customer_gateway, auth_provider_gateway)
    return controller

def test_login_customer_by_cpf(auth_controller, mock_customer_repository, mock_profile_repository):
    customer = Customer(
        id=1,
        person=type('Person', (), {"name": "John Doe", "cpf": "12345678900", "email": "john@example.com"})
    )
    profile = Profile(name="Customer", permissions=[Permission(name="can_create_order")])

    mock_customer_repository.get_by_cpf.return_value = customer
    mock_profile_repository.get_by_name.return_value = profile

    auth_dto = AuthByCpfDTO(cpf="12345678900")

    token_dto = auth_controller.login_customer_by_cpf(auth_dto)

    assert token_dto.access_token is not None
    assert token_dto.token_type == "bearer"

def test_login_customer_by_cpf_not_found(auth_controller, mock_customer_repository):
    mock_customer_repository.get_by_cpf.return_value = None
    auth_dto = AuthByCpfDTO(cpf="12345678900")

    with pytest.raises(EntityNotFoundException, match="Customer not found."):
        auth_controller.login_customer_by_cpf(auth_dto)

def test_login_anonymous(auth_controller, mock_profile_repository, mock_customer_repository):
    profile = Profile(name="Customer", permissions=[Permission(name="view_orders")])
    person = Person(name="Anonymous User", cpf="00000000000", email="anonymous@example.com", birth_date=datetime(2000, 1, 1))
    customer = Customer(id=1, person=person)
    mock_profile_repository.get_by_name.return_value = profile
    mock_customer_repository.create.return_value = customer

    token_dto = auth_controller.login_customer_anonymous()

    assert token_dto.access_token is not None
    assert token_dto.token_type == "bearer"

def test_login_employee(auth_controller, mock_employee_repository, mock_profile_repository):
    role = RoleFactory(name="employee")
    employee = Employee(
        id=1,
        person=type('Person', (), {"name": "Jane Doe", "cpf": "12345678900", "email": "jane@example.com"}),
        user=type('User', (), {"verify_password": lambda password: password == "password123"}),
        role=role
    )
    profile = Profile(name="Employee", permissions=[Permission(name="manage_orders")])

    mock_employee_repository.get_by_username.return_value = employee
    mock_profile_repository.get_by_name.return_value = profile

    login_dto = LoginDTO(username="janedoe", password="password123")
    token_dto =auth_controller.login_employee(login_dto)

    assert token_dto.access_token is not None
    assert token_dto.token_type == "bearer"

def test_login_employee_invalid_credentials(auth_controller, mock_employee_repository):
    mock_employee_repository.get_by_username.return_value = None
    login_dto = LoginDTO(username="janedoe", password="wrongpassword")

    with pytest.raises(InvalidCredentialsException, match="Usuário ou senha inválidos."):
       auth_controller.login_employee(login_dto)

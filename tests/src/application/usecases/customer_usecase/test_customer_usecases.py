import pytest
from datetime import datetime
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.application.usecases.customer_usecase.create_customer_usecase import CreateCustomerUsecase
from src.application.usecases.customer_usecase.get_all_customers_usecase import GetAllCustomersUsecase
from src.adapters.driven.auth_providers.aws_cognito_gateway import AWSCognitoGateway
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.application.usecases.customer_usecase.delete_customer_usecase import DeleteCustomerUsecase
from src.application.usecases.customer_usecase.update_customer_usecase import UpdateCustomerUsecase
from pycpfcnpj import gen

class TestCustomerUsecases:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.customer_gateway = CustomerRepository(db_session)
        self.person_gateway = PersonRepository(db_session)
        self.auth_provider_gateway = AWSCognitoGateway()
        self.create_customer_usecase = CreateCustomerUsecase(self.customer_gateway, self.person_gateway, self.auth_provider_gateway)
        self.update_customer_usecase = UpdateCustomerUsecase(self.customer_gateway, self.person_gateway)
        self.get_all_customers_usecase = GetAllCustomersUsecase(self.customer_gateway)
        self.delete_customer_usecase = DeleteCustomerUsecase(self.customer_gateway)

    def test_create_customer_usecase(self):
        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Doe',
            cpf=cpf,
            email='john@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        dto = CreateCustomerDTO(person=person_dto)
        customer = self.create_customer_usecase.execute(dto)

        assert customer.id is not None
        assert customer.person.name == 'John Doe'
        assert customer.person.cpf == cpf
        assert customer.person.email == 'john@example.com'
        assert customer.person.birth_date is not None

    def test_update_customer_usecase(self):
        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Doe',
            cpf=cpf,
            email='john@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        dto = CreateCustomerDTO(person=person_dto)
        customer = self.create_customer_usecase.execute(dto)

        create_person_dto = CreatePersonDTO(
            name='Jane Doe',
            cpf=cpf,
            email='jane@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        updated_customer_dto = UpdateCustomerDTO(
            id=customer.id,
            person=create_person_dto
        )

        current_user = {
            'profile': {'name': 'manager'},
            'person': {
                'id': customer.person.id,
                'cpf': customer.person.cpf,
                'name': customer.person.name,
                'email': customer.person.email
            }
        }
        customer = self.update_customer_usecase.execute(customer.id, updated_customer_dto, current_user)

        assert customer.person.name == 'Jane Doe'
        assert customer.person.email == 'jane@example.com'
        assert customer.person.birth_date is not None
        assert customer.person.cpf == cpf

    def test_create_duplicate_customer_usecase(self):
        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Doe',
            cpf=cpf,
            email='john@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        dto = CreateCustomerDTO(person=person_dto)
        self.create_customer_usecase.execute(dto)

        with pytest.raises(EntityDuplicatedException):
            self.create_customer_usecase.execute(dto)

    def test_get_all_customers_usecase(self):
        cpf1 = gen.cpf()
        cpf2 = gen.cpf()
        person_dto1 = CreatePersonDTO(
            name='John Doe',
            cpf=cpf1,
            email='john@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        person_dto2 = CreatePersonDTO(
            name='Jane Doe',
            cpf=cpf2,
            email='jane@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        dto1 = CreateCustomerDTO(person=person_dto1)
        dto2 = CreateCustomerDTO(person=person_dto2)

        self.create_customer_usecase.execute(dto1)
        self.create_customer_usecase.execute(dto2)

        current_user = {
            'profile': {'name': 'manager'},
            'person': {'id': '1'}
        }

        customers = self.get_all_customers_usecase.execute(current_user)
        assert len(customers) == 2

    def test_delete_customer_usecase(self):
        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Doe',
            cpf=cpf,
            email='john@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        dto = CreateCustomerDTO(person=person_dto)
        customer = self.create_customer_usecase.execute(dto)

        current_user = {
            'profile': {'name': 'manager'},
            'person': {'id': '1'}
        }

        self.delete_customer_usecase.execute(customer.id, current_user)
        assert customer.is_deleted() is True

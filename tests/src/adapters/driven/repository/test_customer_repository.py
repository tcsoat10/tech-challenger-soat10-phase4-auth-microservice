from datetime import datetime
import pytest
from pycpfcnpj import gen

from src.core.domain.entities.person import Person
from src.adapters.driven.repositories.models.customer_model import CustomerModel
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.core.domain.entities.customer import Customer
from tests.factories.person_factory import PersonFactory
from tests.factories.customer_factory import CustomerFactory


class TestCustomerRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = CustomerRepository(db_session)
        self.db_session = db_session
        self.clean_database()
    
    def clean_database(self):
        self.db_session.query(CustomerModel).delete()
        self.db_session.commit()

    def test_create_customer_success(self):
        person_model = PersonFactory()
        customer = Customer(person=person_model.to_entity())
        created_customer = self.repository.create(customer)

        assert created_customer.id is not None
        assert created_customer.person.id == person_model.id
        
    def test_create_customer_with_person_when_the_person_is_not_registered(self):
        cpf = gen.cpf()
        customer = Customer(
            person=Person(
                name="John Doe",
                cpf=cpf,
                email="jonhdoe@example.com",
                birth_date=datetime(1990, 1, 1)
            )
        )
        created_customer = self.repository.create(customer)
    
        assert created_customer.id is not None
        assert created_customer.person.name == customer.person.name
        assert created_customer.person.cpf == customer.person.cpf
        assert created_customer.person.email == customer.person.email
        assert created_customer.person.birth_date == customer.person.birth_date.date()
    
    def test_get_customer_by_id_success(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_id(customer.id)

        assert customer_response is not None
        assert customer_response.id == customer.id
        assert customer_response.person.id == customer.person_id
    
    def test_get_customer_by_id_returns_none_for_unregistered_id(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_id(customer.id + 1)

        assert customer_response is None

    def test_get_by_cpf_success(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_cpf(customer.person.cpf)

        assert customer_response is not None
        assert customer_response.id == customer.id
        assert customer_response.person.id == customer.person_id

    def test_get_by_cpf_returns_none_for_unregistered_cpf(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_cpf(customer.person.cpf + "1")

        assert customer_response is None

    def test_get_customer_by_person_id_success(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_person_id(customer.person_id)

        assert customer_response is not None
        assert customer_response.id == customer.id
        assert customer_response.person.id == customer.person_id
    
    def test_get_customer_by_person_id_returns_none_for_unregistered_id(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_person_id(customer.person_id + 1)

        assert customer_response is None

    def test_get_all_customers_success(self):
        customer1 = CustomerFactory()
        customer2 = CustomerFactory()

        customers = self.repository.get_all()

        assert len(customers) == 2
        assert customers[0].id == customer1.id
        assert customers[0].person.id == customer1.person_id
        
        assert customers[1].id == customer2.id
        assert customers[1].person.id == customer2.person_id

    def test_get_all_customers_empty_db(self):
        customers = self.repository.get_all()

        assert len(customers) == 0
        assert customers == []

    def test_update_customer(self):
        customer_model = CustomerFactory()
        customer = customer_model.to_entity()
        customer.person.email = "new_email@example.com"

        updated_customer = self.repository.update(customer)

        assert updated_customer.id == customer_model.id
        assert updated_customer.person.id == customer_model.person_id
        assert updated_customer.person.email == "new_email@example.com"

    def test_delete_customer_success(self):
        customer = CustomerFactory()
        
        self.repository.delete(customer)

        customers = self.repository.get_all()

        assert len(customers) == 0
        assert customers == []

    def test_delete_customer_unregistered_id(self):
        customer_model = CustomerFactory()

        person = PersonFactory()
        unregistered_customer = Customer(person=person.to_entity())

        self.repository.delete(unregistered_customer)

        customers = self.repository.get_all()

        assert len(customers) == 1
        assert customers[0].id == customer_model.id
        assert customers[0].person.id == customer_model.person_id
        assert customers[0].person.name == customer_model.person.name
        assert customers[0].person.cpf == customer_model.person.cpf
        assert customers[0].person.email == customer_model.person.email
        assert customers[0].person.birth_date == customer_model.person.birth_date
    
import pytest
from datetime import datetime

from src.adapters.driven.repositories.models.employee_model import EmployeeModel
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.core.domain.entities.employee import Employee
from tests.factories.person_factory import PersonFactory
from tests.factories.role_factory import RoleFactory
from tests.factories.user_factory import UserFactory
from tests.factories.employee_factory import EmployeeFactory


class TestEmployeeRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = EmployeeRepository(db_session)
        self.db_session = db_session
        self.clean_database()
    
    def clean_database(self):
        self.db_session.query(EmployeeModel).delete()
        self.db_session.commit()

    def test_create_employee_success(self):
        person = PersonFactory()
        role = RoleFactory()
        user = UserFactory()
        admission_date = datetime.strptime('01/01/2025', '%d/%m/%Y')
        termination_date = datetime.strptime('12/10/2025', '%d/%m/%Y')

        employee = Employee(
            admission_date=admission_date, 
            termination_date=termination_date,
            person=person.to_entity(),
            role=role.to_entity(),
            user=user.to_entity()
        )

        created_employee = self.repository.create(employee)

        assert created_employee.id is not None
        assert created_employee.admission_date == datetime.date(admission_date)
        assert created_employee.termination_date == datetime.date(termination_date)
        assert created_employee.person.id == person.id
        assert created_employee.role.id == role.id
        assert created_employee.user.id == user.id
    
    def test_get_employee_by_id_success(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_id(employee.id)

        assert employee_response is not None
        assert employee_response.id == employee.id
        assert employee_response.admission_date == employee.admission_date
        assert employee_response.termination_date == employee.termination_date
        assert employee_response.person.id == employee.person_id
        assert employee_response.role.id == employee.role_id
        assert employee_response.user.id == employee.user_id
    
    def test_get_employee_by_person_id_success(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_person_id(employee.person_id)

        assert employee_response is not None
        assert employee_response.id == employee.id
        assert employee_response.admission_date == employee.admission_date
        assert employee_response.termination_date == employee.termination_date
        assert employee_response.person.id == employee.person_id
        assert employee_response.role.id == employee.role_id
        assert employee_response.user.id == employee.user_id

    def test_get_employee_by_user_id_success(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_user_id(employee.user_id)

        assert employee_response is not None
        assert employee_response.id == employee.id
        assert employee_response.admission_date == employee.admission_date
        assert employee_response.termination_date == employee.termination_date
        assert employee_response.person.id == employee.person_id
        assert employee_response.role.id == employee.role_id
        assert employee_response.user.id == employee.user_id

    def test_get_employees_by_role_id_success(self):
        role = RoleFactory()
        employee1 = EmployeeFactory(role=role)
        employee2 = EmployeeFactory(role=role)
        employee3 = EmployeeFactory()
        

        employee_response = self.repository.get_by_role_id(role.id)

        assert employee_response is not None
        assert len(employee_response) == 2
        assert employee_response[0].id == employee1.id
        assert employee_response[1].id == employee2.id
        assert employee_response[0].role.id == role.id
        assert employee_response[1].role.id == role.id

    def test_get_employee_by_id_returns_none_for_unregistered_id(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_id(employee.id + 1)

        assert employee_response is None

    def test_get_employee_by_person_id_returns_none_for_unregistered_id(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_person_id(employee.person_id + 1)

        assert employee_response is None

    def test_get_employee_by_user_id_returns_none_for_unregistered_id(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_user_id(employee.user_id + 1)

        assert employee_response is None

    def test_get_employees_by_role_id_returns_none_for_unregistered_id(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_id(employee.role_id + 1)

        assert employee_response is None

    def test_get_employee_by_username_success(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_username(employee.user.name)

        assert employee_response is not None
        assert employee_response.id == employee.id
        assert employee_response.admission_date == employee.admission_date
        assert employee_response.termination_date == employee.termination_date
        assert employee_response.person.id == employee.person_id
        assert employee_response.role.id == employee.role_id
        assert employee_response.user.id == employee.user_id

    def test_get_employee_by_username_returns_none_for_unregistered_username(self):
        employee = EmployeeFactory()

        employee_response = self.repository.get_by_username(employee.user.name + "1")

        assert employee_response is None

    def test_get_all_employees_success(self):
        employee1 = EmployeeFactory()
        employee2 = EmployeeFactory()

        employees = self.repository.get_all()

        assert len(employees) == 2
        assert employees[0].id == employee1.id
        assert employees[0].person.id == employee1.person_id
        assert employees[0].role.id == employee1.role_id
        assert employees[0].user.id == employee1.user_id
        assert employees[1].id == employee2.id
        assert employees[1].person.id == employee2.person_id
        assert employees[1].role.id == employee2.role_id
        assert employees[1].user.id == employee2.user_id

    def test_get_all_customers_empty_db(self):
        employees = self.repository.get_all()

        assert len(employees) == 0
        assert employees == []

    def test_update_employee(self):
        employee_model = EmployeeFactory()
        person = PersonFactory()
        role = RoleFactory()
        user = UserFactory()
        
        employee = employee_model.to_entity()
        employee.person = person.to_entity()
        employee.role = role.to_entity()
        employee.user = user.to_entity()

        data = self.repository.update(employee)

        assert data.id == employee.id
        assert data.person.id == person.id
        assert data.role.id == role.id
        assert data.user.id == user.id

    def test_delete_employee(self):
        employee = EmployeeFactory()

        self.repository.delete(employee.id)

        data = self.repository.get_all()

        assert len(data) == 0
        assert data == []

    def test_delete_employee_unregistered_id(self):
        employee = EmployeeFactory()

        self.repository.delete(employee.id + 1)

        data = self.repository.get_all()

        assert len(data) == 1
        assert data[0].id == employee.id
        assert data[0].person.id == employee.person_id
        assert data[0].role.id == employee.role_id
        assert data[0].user.id == employee.user_id

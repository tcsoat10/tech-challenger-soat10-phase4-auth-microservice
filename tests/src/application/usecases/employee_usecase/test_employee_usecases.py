import pytest
from datetime import datetime
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.application.usecases.employee_usecase.create_employee_usecase import CreateEmployeeUseCase
from src.application.usecases.employee_usecase.update_employee_usecase import UpdateEmployeeUseCase
from src.application.usecases.employee_usecase.delete_employee_usecase import DeleteEmployeeUseCase
from src.application.usecases.employee_usecase.get_all_employees_usecase import GetAllEmployeesUseCase
from pycpfcnpj import gen
from src.core.domain.entities.role import Role
from src.core.domain.entities.user import User

class TestEmployeeUsecases:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.employee_gateway = EmployeeRepository(db_session)
        self.person_gateway = PersonRepository(db_session)
        self.role_gateway = RoleRepository(db_session)
        self.user_gateway = UserRepository(db_session)
        
        self.create_employee_usecase = CreateEmployeeUseCase(
            self.employee_gateway, 
            self.person_gateway, 
            self.role_gateway, 
            self.user_gateway
        )
        self.update_employee_usecase = UpdateEmployeeUseCase(
            self.employee_gateway, 
            self.person_gateway, 
            self.role_gateway, 
            self.user_gateway
        )
        self.delete_employee_usecase = DeleteEmployeeUseCase(self.employee_gateway)
        self.get_all_employees_usecase = GetAllEmployeesUseCase(self.employee_gateway)

    def test_create_employee_usecase(self):
        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Employee',
            cpf=cpf,
            email='john.employee@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        role = Role(name='cashier', description='Cashier role')
        role = self.role_gateway.create(role)

        user = User(name='john.employee', password='pass123')
        user = self.user_gateway.create(user)

        dto = CreateEmployeeDTO(
            person=person_dto,
            role_id=role.id,
            user_id=user.id
        )

        employee = self.create_employee_usecase.execute(dto)

        assert employee.id is not None
        assert employee.person.name == 'John Employee'
        assert employee.role.name == 'cashier'
        assert employee.user.name == 'john.employee'

    def test_create_duplicate_employee_usecase(self):
        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Employee',
            cpf=cpf,
            email='john.employee@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        role = Role(name='cashier', description='Cashier role')
        role = self.role_gateway.create(role)

        user = User(name='john.employee', password='pass123')
        user = self.user_gateway.create(user)

        dto = CreateEmployeeDTO(
            person=person_dto,
            role_id=role.id,
            user_id=user.id
        )

        self.create_employee_usecase.execute(dto)

        with pytest.raises(EntityDuplicatedException):
            self.create_employee_usecase.execute(dto)

    def test_get_all_employees_usecase(self):
        role = Role(name='cashier', description='Cashier role')
        role = self.role_gateway.create(role)

        # Create first employee
        cpf1 = gen.cpf()
        person_dto1 = CreatePersonDTO(
            name='John Employee',
            cpf=cpf1,
            email='john.employee@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )
        user1 = User(name='john.employee', password='pass123')
        user1 = self.user_gateway.create(user1)
        dto1 = CreateEmployeeDTO(person=person_dto1, role_id=role.id, user_id=user1.id)

        # Create second employee
        cpf2 = gen.cpf()
        person_dto2 = CreatePersonDTO(
            name='Jane Employee',
            cpf=cpf2,
            email='jane.employee@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )
        user2 = User(name='jane.employee', password='pass123')
        user2 = self.user_gateway.create(user2)
        dto2 = CreateEmployeeDTO(person=person_dto2, role_id=role.id, user_id=user2.id)

        self.create_employee_usecase.execute(dto1)
        self.create_employee_usecase.execute(dto2)

        employees = self.get_all_employees_usecase.execute()
        assert len(employees) == 2

    def test_delete_employee_usecase(self):
        role = Role(name='cashier', description='Cashier role')
        role = self.role_gateway.create(role)

        user = User(name='john.employee', password='pass123')
        user = self.user_gateway.create(user)

        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Employee',
            cpf=cpf,
            email='john.employee@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        dto = CreateEmployeeDTO(person=person_dto, role_id=role.id, user_id=user.id)
        employee = self.create_employee_usecase.execute(dto)

        self.delete_employee_usecase.execute(employee.id)
        assert employee.is_deleted() is True

    def test_update_employee_usecase(self):
        role1 = Role(name='cashier', description='Cashier role')
        role1 = self.role_gateway.create(role1)
        role2 = Role(name='manager', description='Manager role')
        role2 = self.role_gateway.create(role2)

        user = User(name='john.employee', password='pass123')
        user = self.user_gateway.create(user)

        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Employee',
            cpf=cpf,
            email='john.employee@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        create_dto = CreateEmployeeDTO(person=person_dto, role_id=role1.id, user_id=user.id)
        employee = self.create_employee_usecase.execute(create_dto)

        update_dto = UpdateEmployeeDTO(
            id=employee.id,
            person_id=employee.person.id,
            role_id=role2.id,
            user_id=user.id
        )

        updated_employee = self.update_employee_usecase.execute(employee.id, update_dto)
        assert updated_employee.role.name == 'manager'

    def test_update_employee_not_found_usecase(self):
        role = Role(name='cashier', description='Cashier role')
        role = self.role_gateway.create(role)

        user = User(name='john.employee', password='pass123')
        user = self.user_gateway.create(user)

        update_dto = UpdateEmployeeDTO(
            id=1,
            person_id=1,
            role_id=role.id,
            user_id=user.id
        )
        
        with pytest.raises(EntityNotFoundException):
            self.update_employee_usecase.execute(1, update_dto)

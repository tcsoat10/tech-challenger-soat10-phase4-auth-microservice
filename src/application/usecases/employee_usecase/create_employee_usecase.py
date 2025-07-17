
from src.core.domain.entities.person import Person
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.entities.employee import Employee
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class CreateEmployeeUseCase:
    
    def __init__(
        self,
        employee_gateway: IEmployeeRepository,
        person_gateway: IPersonRepository,
        role_gateway: IRoleRepository,
        user_gateway: IUserRepository,
    ):
        self.employee_gateway = employee_gateway
        self.person_gateway = person_gateway
        self.role_gateway = role_gateway
        self.user_gateway = user_gateway

    @classmethod
    def build(
        cls,
        employee_gateway: IEmployeeRepository,
        person_gateway: IPersonRepository,
        role_gateway: IRoleRepository,
        user_gateway: IUserRepository,
    ) -> 'CreateEmployeeUseCase':
        return cls(employee_gateway, person_gateway, role_gateway, user_gateway)

    def execute(self, dto: CreateEmployeeDTO) -> Employee:
        person = self.person_gateway.get_by_cpf(dto.person.cpf)
        if not person:
            if self.person_gateway.exists_by_email(dto.person.email):
                raise EntityDuplicatedException(entity_name='Person')

            person = Person(
                name=dto.person.name,
                cpf=dto.person.cpf,
                email=dto.person.email,
                birth_date=dto.person.birth_date
            )
            person = self.person_gateway.create(person)
        else:
            person.name = dto.person.name
            person.email = dto.person.email
            person.birth_date = dto.person.birth_date
            if person.is_deleted():
                person.reactivate()
            self.person_gateway.update(person)
        
        person = self.person_gateway.get_by_cpf(dto.person.cpf)
        if not person:
            raise EntityNotFoundException(entity_name='Person')

        role = self.role_gateway.get_by_id(dto.role_id)
        if not role:
            raise EntityNotFoundException(entity_name='Role')

        user = self.user_gateway.get_by_id(dto.user_id)
        if not user:
            raise EntityNotFoundException(entity_name='User')

        existing_employee_by_user = self.employee_gateway.get_by_username(user.name)
        if existing_employee_by_user:
            if not existing_employee_by_user.is_deleted():
                raise EntityDuplicatedException(entity_name='Employee')

        existing_employee_by_person = self.employee_gateway.get_by_person_id(person.id)
        if existing_employee_by_person:
            if not existing_employee_by_person.is_deleted():
                raise EntityDuplicatedException(entity_name='Employee')

        if existing_employee_by_user:
            employee = existing_employee_by_user
            employee.person = person
            employee.role = role
            employee.user = user
            employee.reactivate()
            self.employee_gateway.update(employee)
        else:
            employee = Employee(person=person, role=role, user=user)
            employee = self.employee_gateway.create(employee)

        return employee


from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO
from src.core.domain.entities.employee import Employee
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.employee.i_employee_repository import IEmployeeRepository


class UpdateEmployeeUseCase:
    
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
    ) -> 'UpdateEmployeeUseCase':
        return cls(
            employee_gateway=employee_gateway,
            person_gateway=person_gateway,
            role_gateway=role_gateway,
            user_gateway=user_gateway,
        )
    
    def _get_entity(self, repository, entity_id, entity_name):
        entity = repository.get_by_id(entity_id)
        if not entity:
            raise EntityNotFoundException(entity_name=entity_name)
        return entity

    def execute(self, employee_id: int, dto: UpdateEmployeeDTO) -> Employee:
        employee = self._get_entity(self.employee_gateway, employee_id, 'Employee')
        if employee.is_deleted():
            raise EntityNotFoundException(entity_name='Employee')
        
        employee.person = self._get_entity(self.person_gateway, dto.person_id, 'Person')
        employee.role = self._get_entity(self.role_gateway, dto.role_id, 'Role')
        employee.user = self._get_entity(self.user_gateway, dto.user_id, 'User')
        
        return self.employee_gateway.update(employee)

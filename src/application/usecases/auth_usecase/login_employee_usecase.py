
from typing import Any, Dict

from src.core.domain.dtos.auth.auth_dto import LoginDTO
from src.core.domain.entities.employee import Employee
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.invalid_credentials_exception import InvalidCredentialsException
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.utils.jwt_util import JWTUtil


class LoginEmployeeUseCase:
    
    def __init__(self, employee_gateway: IEmployeeRepository, profile_gateway: IProfileRepository):
        self.employee_gateway = employee_gateway
        self.profile_gateway = profile_gateway
        
    @classmethod
    def build(cls, employee_gateway: IEmployeeRepository, profile_gateway: IProfileRepository) -> "LoginEmployeeUseCase":
        return cls(employee_gateway, profile_gateway)
    
    def execute(self, login_dto: LoginDTO) -> Dict[str, Any]:
        employee: Employee = self.employee_gateway.get_by_username(login_dto.username)
        if not employee or not employee.user.verify_password(login_dto.password):
            raise InvalidCredentialsException()
        
        if employee.is_deleted():
            raise InvalidCredentialsException()
        
        profile_name = 'employee'
        if employee.role.name == 'manager':
            profile_name = 'manager'

        employee_profile = self.profile_gateway.get_by_name(profile_name)
        if not employee_profile:
            raise EntityNotFoundException(entity_name="Employee profile")
 
        permissions = [permission.name for permission in employee_profile.permissions]
        if not permissions:
            raise EntityNotFoundException(entity_name="Employee permissions")

        token_payload = {
            "person": {
                "id": str(employee.id),
                "name": employee.person.name,
                "cpf": employee.person.cpf,
                "email": employee.person.email,
            },
            "profile": {
                "name": employee_profile.name,
                "permissions": permissions,
            },
        }

        token = JWTUtil.create_token(token_payload)
        return {
            "token_type": "bearer",
            "access_token": token
        }

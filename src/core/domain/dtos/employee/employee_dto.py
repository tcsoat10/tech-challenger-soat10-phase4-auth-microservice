from pydantic import BaseModel

from src.core.domain.dtos.person.person_dto import PersonDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.core.domain.dtos.user.user_dto import UserDTO
from src.core.domain.entities.employee import Employee


class EmployeeDTO(BaseModel):
    id: int
    person: PersonDTO
    role: RoleDTO
    user: UserDTO

    @classmethod
    def from_entity(cls, employee: Employee) -> 'EmployeeDTO':
        return cls(
            id=employee.id,
            person=PersonDTO.from_entity(employee.person),
            role=RoleDTO.from_entity(employee.role),
            user=UserDTO.from_entity(employee.user)
        )
    
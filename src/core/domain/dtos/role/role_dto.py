from pydantic import BaseModel

from src.core.domain.entities.role import Role


class RoleDTO(BaseModel):
    id: int
    name: str
    description: str

    @classmethod
    def from_entity(cls, role: Role) -> 'RoleDTO':
        return cls(id=role.id, name=role.name, description=role.description)
    
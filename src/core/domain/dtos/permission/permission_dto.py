from pydantic import BaseModel
from src.core.domain.entities.permission import Permission


class PermissionDTO(BaseModel):
    id: int
    name: str
    description: str

    @classmethod
    def from_entity(cls, permission: Permission) -> 'PermissionDTO':
        return cls(id=permission.id, name=permission.name, description=permission.description)
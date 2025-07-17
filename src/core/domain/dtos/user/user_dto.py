from pydantic import BaseModel

from src.core.domain.entities.user import User


class UserDTO(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, user: User) -> 'UserDTO':
        return cls(id=user.id, name=user.name)
from pydantic import BaseModel
from src.core.domain.entities.profile import Profile


class ProfileDTO(BaseModel):
    id: int
    name: str
    description: str

    @classmethod
    def from_entity(cls, profile: Profile) -> 'ProfileDTO':
        return cls(id=profile.id, name=profile.name, description=profile.description)
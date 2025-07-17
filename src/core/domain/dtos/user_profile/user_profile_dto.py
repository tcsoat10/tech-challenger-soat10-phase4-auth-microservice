
from pydantic import BaseModel

from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.core.domain.dtos.user.user_dto import UserDTO
from src.core.domain.entities.user_profile import UserProfile


class UserProfileDTO(BaseModel):
    id: int
    user: UserDTO
    profile: ProfileDTO

    @classmethod
    def from_entity(cls, user_profile: UserProfile) -> "UserProfileDTO":
        return cls(
            id=user_profile.id,
            user=UserDTO.from_entity(user_profile.user),
            profile=ProfileDTO.from_entity(user_profile.profile)
        )

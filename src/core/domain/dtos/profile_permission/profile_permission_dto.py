from pydantic import BaseModel

from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.core.domain.entities.profile_permission import ProfilePermission


class ProfilePermissionDTO(BaseModel):
    id: int
    permission: PermissionDTO
    profile: ProfileDTO

    @classmethod
    def from_entity(cls, profile_permission: ProfilePermission) -> 'ProfilePermissionDTO':
        return cls(
            id=profile_permission.id,
            permission=PermissionDTO.from_entity(profile_permission.permission),
            profile=ProfileDTO.from_entity(profile_permission.profile)
        )

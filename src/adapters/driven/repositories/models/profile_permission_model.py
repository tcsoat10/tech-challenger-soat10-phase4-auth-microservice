from src.core.domain.entities.profile_permission import ProfilePermission
from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class ProfilePermissionModel(BaseModel):
    __tablename__ = 'profile_permissions'

    profile_id = Column(ForeignKey('profiles.id'), nullable=False)
    profile = relationship('ProfileModel', back_populates='profile_permissions', overlaps="permissions,profiles")

    permission_id = Column(ForeignKey('permissions.id'), nullable=False)
    permission = relationship('PermissionModel', back_populates='profile_permissions', overlaps="profiles,permissions")

    @classmethod
    def from_entity(cls, entity: ProfilePermission) -> 'ProfilePermissionModel':
        return cls(
            id=entity.id,
            profile_id=entity.profile.id,
            permission_id=entity.permission.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            inactivated_at=entity.inactivated_at
        )

    def to_entity(self):
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(ProfilePermission, self.id)
        if existing:
            return existing

        profile_permission = ProfilePermission(
            id=self.id,
            profile=self.profile,
            permission=self.permission,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(profile_permission)
        return profile_permission


__all__ = ['ProfilePermissionModel']

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.profile import Profile
from src.core.shared.identity_map import IdentityMap


class ProfileModel(BaseModel):
    __tablename__ = "profiles"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    profile_permissions = relationship("ProfilePermissionModel", back_populates="profile", overlaps="permissions")
    permissions = relationship("PermissionModel", secondary="profile_permissions", back_populates="profiles", overlaps="profile_permissions")

    user_profiles = relationship("UserProfileModel", back_populates="profile", overlaps="users")

    def _import_user_model(): #Alterado para UserModel
        from src.adapters.driven.repositories.models.user_model import UserModel
        return UserModel

    users = relationship(_import_user_model, secondary="user_profiles", back_populates="profiles") #Alterado para UserModel

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            inactivated_at=entity.inactivated_at
        )

    def to_entity(self):
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(Profile, self.id)
        if existing:
            return existing

        profile = Profile(
            id=self.id,
            name=self.name,
            profile_permissions=[profile_permission.to_entity() for profile_permission in self.profile_permissions],
            permissions=[permission.to_entity() for permission in self.permissions],
            # user_profiles=[user_profile.to_entity() for user_profile in self.user_profiles],
            users=[user.to_entity() for user in self.users],
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(profile)
        return profile


__all__ = ["ProfileModel"]

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.user_profile import UserProfile
from src.core.shared.identity_map import IdentityMap


class UserProfileModel(BaseModel):
    __tablename__ = "user_profiles"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="user_profiles", overlaps="profiles,users") #Alterado para UserModel
    profile_id = Column(ForeignKey("profiles.id"), nullable=False)
    profile = relationship("ProfileModel", back_populates="user_profiles", overlaps="users,profiles")

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            user_id=entity.user.id,
            profile_id=entity.profile.id,
        )

    def to_entity(self):
        
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(UserProfile, self.id)
        if existing:
            return existing
        
        user_entity = self._get_user_entity()
        profile_entity = self._get_profile_entity()

        user_profile = UserProfile(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
            user=user_entity,
            profile=profile_entity,
        )
        identity_map.add(user_profile)
        return user_profile

    def _get_user_entity(self):
        from src.core.domain.entities.user import User
        
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_user = identity_map.get(User, self.user_id)
        if existing_user:
            return existing_user
        return self.user.to_entity()

    def _get_profile_entity(self):
        from src.core.domain.entities.profile import Profile
        
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_profile = identity_map.get(Profile, self.profile_id)
        if existing_profile:
            return existing_profile
        return self.profile.to_entity()

__all__ = ["UserProfileModel"]

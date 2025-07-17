
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.user import User
from src.core.shared.identity_map import IdentityMap


class UserModel(BaseModel):
    __tablename__ = "users"

    name = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False, unique=False)

    user_profiles = relationship("UserProfileModel", back_populates="user", overlaps="profiles,users")
    profiles = relationship("ProfileModel", secondary="user_profiles", back_populates="users", overlaps="user_profiles")


    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            name=entity.name,
            password_hash=entity.password_hash,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            inactivated_at=entity.inactivated_at
        )

    def to_entity(self):
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(User, self.id)
        if existing:
            return existing

        user = User(
            id=self.id,
            name=self.name,
            password_hash=self.password_hash,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(user)
        return user

__all__ = ["UserModel"]

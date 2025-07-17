from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.permission import Permission
from src.core.shared.identity_map import IdentityMap


class PermissionModel(BaseModel):
    __tablename__ = "permissions"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    profile_permissions = relationship("ProfilePermissionModel", back_populates="permission", overlaps="profiles")
    profiles = relationship("ProfileModel", secondary="profile_permissions", back_populates="permissions", overlaps="profile_permissions")


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

    def to_entity(self) -> Permission:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(Permission, self.id)
        if existing:
            return existing

        permission = Permission(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(permission)
        return permission


__all__ = ["PermissionModel"]

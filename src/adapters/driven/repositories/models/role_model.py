from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.role import Role
from src.adapters.driven.repositories.models.base_model import BaseModel

from sqlalchemy import Column, String



class RoleModel(BaseModel):
    __tablename__ = 'roles'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(100))
    
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
        existing = identity_map.get(Role, self.id)
        if existing:
            return existing
        
        return Role(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        

__all__ = ['RoleModel']

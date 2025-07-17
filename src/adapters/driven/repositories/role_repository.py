from src.core.shared.identity_map import IdentityMap
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.entities.role import Role
from src.adapters.driven.repositories.models.role_model import RoleModel

from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import exists


class RoleRepository(IRoleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, role: Role) -> Role:
        if role.id is not None:
            existing = self.identity_map.get(Role, role.id)
            if existing:
                self.identity_map.remove(existing)
                
        role_model = RoleModel.from_entity(role)    
        self.db_session.add(role_model)
        self.db_session.commit()
        self.db_session.refresh(role_model)
        return role_model.to_entity()
    
    def get_by_name(self, name: str) -> Role:
        role_model = (
            self.db_session
                .query(RoleModel)
                .filter(RoleModel.name == name)
                .first()
        )
        if role_model is None:
            return None
        return role_model.to_entity()
    
    def get_by_id(self, role_id: int) -> Role:
        role_model = (
            self.db_session
                .query(RoleModel)
                .filter(RoleModel.id == role_id)
                .first()
        )
        if role_model is None:
            return None
        return role_model.to_entity()
    
    def get_all(self, include_deleted: bool = False) -> List[Role]:
        query = self.db_session.query(RoleModel)
        if not include_deleted:
            query = query.filter(RoleModel.inactivated_at.is_(None))
        role_models = query.all()
        return [role_model.to_entity() for role_model in role_models]
    
    def update(self, role: Role) -> Role:
        if role.id is not None:
            existing = self.identity_map.get(Role, role.id)
            if existing:
                self.identity_map.remove(existing)
        
        role_model = RoleModel.from_entity(role)
        self.db_session.merge(role_model)
        self.db_session.commit()
        return role_model.to_entity()
    
    def delete(self, role: int) -> None:
        role_model = (
            self.db_session
                .query(RoleModel)
                .filter(RoleModel.id == role.id)
                .first()
        )
        if role_model:
            self.db_session.delete(role_model)
            self.db_session.commit()
            self.identity_map.remove(role)

    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(Role.name == name)).scalar()

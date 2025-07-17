from src.adapters.driven.repositories.models.permission_model import PermissionModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.permission import Permission
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List

class PermissionRepository(IPermissionRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, permission: Permission) -> Permission:
        if permission.id is not None:
            existing = self.identity_map.get(Permission, permission.id)
            if existing:
                self.identity_map.remove(existing)
        
        permission_model = PermissionModel.from_entity(permission)
        self.db_session.add(permission_model)
        self.db_session.commit()
        self.db_session.refresh(permission_model)
        return permission_model.to_entity()
    
    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(PermissionModel.name == name)).scalar()
    
    def get_by_name(self, name: str) -> Permission:
        permission_model = self.db_session.query(PermissionModel).filter(PermissionModel.name == name).first()
        if not permission_model:
            return None
        return permission_model.to_entity()
    
    def get_by_id(self, permission_id: int) -> Permission:
        permission_model = self.db_session.query(PermissionModel).filter(PermissionModel.id == permission_id).first()
        if not permission_model:
            return None
        return permission_model.to_entity()
    
    def get_all(self, include_deleted: bool = False) -> List[Permission]:
        query = self.db_session.query(PermissionModel)
        if not include_deleted:
            query = query.filter(PermissionModel.inactivated_at.is_(None))
        permission_models = query.all()
        return [permission_model.to_entity() for permission_model in permission_models]
    
    def update(self, permission: Permission) -> Permission:
        if permission.id is not None:
            existing = self.identity_map.get(Permission, permission.id)
            if existing:
                self.identity_map.remove(existing)
                
        permission_model = PermissionModel.from_entity(permission)
        self.db_session.merge(permission_model)
        self.db_session.commit()
        return permission_model.to_entity()
    
    def delete(self, permission: Permission) -> None:
        permission_model = (
            self.db_session.query(PermissionModel)
                .filter(PermissionModel.id == permission.id)
                .first()
        )

        if permission_model:
            self.db_session.delete(permission_model)
            self.db_session.commit()
            self.identity_map.remove(permission)

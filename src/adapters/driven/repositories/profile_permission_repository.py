from src.adapters.driven.repositories.models.profile_permission_model import ProfilePermissionModel
from src.core.shared.identity_map import IdentityMap
from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.domain.entities.profile_permission import ProfilePermission

from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List


class ProfilePermissionRepository(IProfilePermissionRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()
    
    def create(self, profile_permission: ProfilePermission) -> ProfilePermission:
        if profile_permission.id is not None:
            existing = self.get_by_id(profile_permission.id)
            if existing:
                self.identity_map.remove(existing)
        
        profile_permission_model = ProfilePermissionModel.from_entity(profile_permission)
        self.db_session.add(profile_permission_model)
        self.db_session.commit()
        self.db_session.refresh(profile_permission_model)
        return profile_permission_model.to_entity()
    
    def exists_by_permission_id_and_profile_id(self, permission_id: int, profile_id: int) -> bool:
        return (
            self.db_session.query(
                exists()
                .where(ProfilePermission.permission_id == permission_id and ProfilePermission.profile_id == profile_id)
            )
            .first()
        )
    
    def get_by_id(self, profile_permission_id: int) -> ProfilePermission:
        profile_permission_model = (
            self.db_session.query(ProfilePermissionModel)
                .filter(ProfilePermissionModel.id == profile_permission_id)
                .first()
        )
        if not profile_permission_model:
            return None
        return profile_permission_model.to_entity()
    
    def get_by_permission_id_and_profile_id(self, permission_id: int, profile_id: int) -> ProfilePermission:
        profile_permission_model = (
            self.db_session.query(ProfilePermissionModel)
            .filter(ProfilePermissionModel.permission_id == permission_id, ProfilePermissionModel.profile_id == profile_id)
            .first()
        )
        if not profile_permission_model:
            return None
        return profile_permission_model.to_entity()

    def get_by_profile_id(self, profile_id: int) -> ProfilePermission:
        profile_permission_model = (
            self.db_session.query(ProfilePermissionModel)
                .filter(ProfilePermissionModel.profile_id == profile_id)
                .first()
        )
        if not profile_permission_model:
            return None
        return profile_permission_model.to_entity()
    
    def get_by_permission_id(self, permission_id: int) -> ProfilePermission:
        profile_permission_model = (
            self.db_session.query(ProfilePermissionModel)
                .filter(ProfilePermissionModel.permission_id == permission_id)
                .first()
        )
        if not profile_permission_model:
            return None
        return profile_permission_model.to_entity()
    
    def get_all(self, include_deleted: bool = False) -> List[ProfilePermission]:
        query = self.db_session.query(ProfilePermissionModel)
        if not include_deleted:
            query = query.filter(ProfilePermissionModel.inactivated_at.is_(None))
        profile_permission_models = query.all()
        return [ppm.to_entity() for ppm in profile_permission_models]
    
    def update(self, profile_permission: ProfilePermission) -> ProfilePermission:
        from src.adapters.driven.repositories.models.permission_model import PermissionModel
        from src.adapters.driven.repositories.models.profile_model import ProfileModel
        
        if profile_permission.id is not None:
            existing = self.get_by_id(profile_permission.id)
            if existing:
                self.identity_map.remove(existing)

        profile_permission_model = ProfilePermissionModel.from_entity(profile_permission)
        profile_permission_model.profile = ProfileModel.from_entity(profile_permission.profile)
        profile_permission_model.permission = PermissionModel.from_entity(profile_permission.permission)

        self.db_session.merge(profile_permission_model)
        self.db_session.commit()
        return profile_permission_model.to_entity()
    
    def delete(self, profile_permission: ProfilePermission) -> None:
        profile_permission_model = (
            self.db_session.query(ProfilePermissionModel)
                .filter(ProfilePermissionModel.id == profile_permission.id)
                .first()
        )
        
        if profile_permission_model:
            self.db_session.delete(profile_permission)
            self.db_session.commit()
            self.identity_map.remove(profile_permission)

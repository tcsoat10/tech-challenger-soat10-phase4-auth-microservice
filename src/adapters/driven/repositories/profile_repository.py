from src.adapters.driven.repositories.models.profile_model import ProfileModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.profile import Profile
from src.core.ports.profile.i_profile_repository import IProfileRepository
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List

class ProfileRepository(IProfileRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, profile: Profile) -> Profile:
        if profile.id is not None:
            existing = self.identity_map.get(Profile, profile.id)
            if existing:
                self.identity_map.remove(existing)
                
        profile_model = ProfileModel.from_entity(profile)
        self.db_session.add(profile_model)
        self.db_session.commit()
        self.db_session.refresh(profile_model)
        return profile_model.to_entity()
    
    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(ProfileModel.name == name)).scalar()
    
    def get_by_name(self, name: str) -> Profile:
        profile_model = self.db_session.query(ProfileModel).filter(ProfileModel.name == name).first()
        if not profile_model:
            return None
        return profile_model.to_entity()
    
    def get_by_id(self, profile_id: int) -> Profile:
        profile_model = self.db_session.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if not profile_model:
            return None
        return profile_model.to_entity()
    
    def get_all(self, include_deleted: bool = False) -> List[Profile]:
        query = self.db_session.query(ProfileModel)
        if not include_deleted:
            query = query.filter(ProfileModel.inactivated_at.is_(None))
        profile_models = query.all()
        return [profile_model.to_entity() for profile_model in profile_models]
    
    def update(self, profile: Profile) -> Profile:
        if profile.id is not None:
            existing = self.identity_map.get(Profile, profile.id)
            if existing:
                self.identity_map.remove(existing)
                
        profile_model = ProfileModel.from_entity(profile)
        self.db_session.merge(profile_model)
        self.db_session.commit()
        return profile_model.to_entity()
    
    def delete(self, profile_id: int) -> None:
        profile_model = self.db_session.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if profile_model:
            self.db_session.delete(profile_model)
            self.db_session.commit()
            self.identity_map.remove(profile_model)

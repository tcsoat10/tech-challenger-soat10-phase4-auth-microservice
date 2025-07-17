from typing import Optional
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.models.user_profile_model import UserProfileModel
from src.core.shared.identity_map import IdentityMap
from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.domain.entities.user_profile import UserProfile



class UserProfileRepository(IUserProfileRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, user_profile: UserProfile) -> UserProfile:
        if user_profile.id is not None:
            existing = self.identity_map.get(UserProfile, user_profile.id)
            if existing:
                self.identity_map.remove(existing)
        
        user_profile_model = UserProfileModel.from_entity(user_profile)
        self.db_session.add(user_profile_model)
        self.db_session.commit()
        return user_profile_model.to_entity()
    
    def get_by_id(self, id: int) -> UserProfile:
        user_profile_model = self.db_session.query(UserProfileModel).filter_by(id=id).first()
        if not user_profile_model:
            return None
        return user_profile_model.to_entity()

    def get_by_user_id_and_profile_id(self, user_id: int, profile_id: int) -> UserProfile:
        user_profile_model = self.db_session.query(UserProfileModel).filter_by(user_id=user_id, profile_id=profile_id).first()
        if not user_profile_model:
            return None
        return user_profile_model.to_entity()
    
    def get_all(self, include_deleted: Optional[bool] = False) -> list[UserProfile]:
        query = self.db_session.query(UserProfileModel)
        if not include_deleted:
            query = query.filter(UserProfileModel.inactivated_at.is_(None))
        user_profile_models = query.all()
        return [user_profile_model.to_entity() for user_profile_model in user_profile_models]
    
    def update(self, user_profile: UserProfile) -> UserProfile:
        if user_profile.id is not None:
            existing = self.identity_map.get(UserProfile, user_profile.id)
            if existing:
                self.identity_map.remove(existing)
        
        user_profile_model = UserProfileModel.from_entity(user_profile)
        self.db_session.merge(user_profile_model)
        self.db_session.commit()
        return user_profile_model.to_entity()
    
    def delete(self, user_profile: UserProfile) -> None:
        user_profile_model = self.db_session.query(UserProfileModel).filter_by(id=user_profile.id).first()
        if user_profile_model:
            self.db_session.delete(user_profile_model)
            self.db_session.commit()
            self.identity_map.remove(user_profile)

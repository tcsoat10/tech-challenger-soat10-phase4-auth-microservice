from src.adapters.driven.repositories.models.user_model import UserModel
from src.core.shared.identity_map import IdentityMap
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.entities.user import User

from sqlalchemy.orm import Session
from typing import List


class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, user: User) -> User:
        if user.id is not None:
            existing = self.get_by_id(user.id)
            if existing:
                self.identity_map.remove(existing)
        
        user_model = UserModel.from_entity(user)
        self.db_session.add(user_model)
        self.db_session.commit()
        self.db_session.refresh(user_model)
        return user_model.to_entity()
    
    def get_by_name(self, name: str) -> User:
        user_model = self.db_session.query(UserModel).filter(UserModel.name == name).first()
        if not user_model:
            return None
        return user_model.to_entity()
    
    def get_by_id(self, user_id: int) -> User:
        user_model = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        return user_model.to_entity()

    def get_all(self, include_deleted: bool = False) -> List[User]:
        query =  self.db_session.query(UserModel)
        if not include_deleted:
            query = query.filter(UserModel.inactivated_at.is_(None))
        user_models = query.all()
        return [user_model.to_entity() for user_model in user_models]
    
    def update(self, user: User) -> User:
        if user.id is not None:
            existing = self.identity_map.get(User, user.id)
            if existing:
                self.identity_map.remove(existing)
        
        user_model = UserModel.from_entity(user)
        self.db_session.merge(user_model)
        self.db_session.commit()
        return user_model.to_entity()
    
    def delete(self, user_id: int) -> None:
        user_model = (
            self.db_session.query(UserModel)
                .filter(UserModel.id == user_id)
                .first()
        )
        if user_model:
            self.db_session.delete(user_model)
            self.db_session.commit()
            self.identity_map.remove(user_model.to_entity())

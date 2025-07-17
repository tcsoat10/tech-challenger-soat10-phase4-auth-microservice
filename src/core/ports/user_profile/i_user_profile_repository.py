from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.entities.user_profile import UserProfile

class IUserProfileRepository(ABC):

    @abstractmethod
    def create(self, user_profile: UserProfile) -> UserProfile:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> UserProfile:
        pass

    @abstractmethod
    def get_by_user_id_and_profile_id(self, user_id: int, profile_id: int) -> UserProfile:
        pass

    @abstractmethod
    def get_all(self, include_deleted: Optional[bool]) -> list[UserProfile]:
        pass

    @abstractmethod
    def update(self, user_profile: UserProfile) -> UserProfile:
        pass

    @abstractmethod
    def delete(self, user_profile: UserProfile) -> None:
        pass

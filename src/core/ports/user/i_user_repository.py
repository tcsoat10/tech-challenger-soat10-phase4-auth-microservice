from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def create(user: User):
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
    
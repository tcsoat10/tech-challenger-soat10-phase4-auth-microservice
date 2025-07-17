from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.role import Role


class IRoleRepository(ABC):
    @abstractmethod
    def create(role: Role):
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Role:
        pass

    @abstractmethod
    def get_by_id(self, role_id: int) -> Role:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Role]:
        pass

    @abstractmethod
    def update(self, role: Role) -> Role:
        pass

    @abstractmethod
    def delete(self, role: Role) -> None:
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

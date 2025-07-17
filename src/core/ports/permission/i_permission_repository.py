from abc import ABC, abstractmethod

from src.core.domain.entities.permission import Permission


class IPermissionRepository(ABC):

    @abstractmethod
    def create(permission: Permission):
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Permission:
        pass

    @abstractmethod
    def get_by_id(self, permission_id: int) -> Permission:
        pass
    
    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> Permission:
        pass

    @abstractmethod
    def update(self, permission: Permission) -> Permission:
        pass

    @abstractmethod
    def delete(self, permission: Permission) -> None:
        pass

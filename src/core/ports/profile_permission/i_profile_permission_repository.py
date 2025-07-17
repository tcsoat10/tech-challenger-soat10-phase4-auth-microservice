from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.profile_permission import ProfilePermission


class IProfilePermissionRepository(ABC):
    @abstractmethod
    def create(profile_permission: ProfilePermission):
        pass

    def exists_by_permission_id_and_profile_id(self, permission_id: int, profile_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_id(self, profile_permission_id: int) -> ProfilePermission:
        pass

    @abstractmethod
    def get_by_permission_id_and_profile_id(self, permission_id: int, profile_id: int) -> ProfilePermission:
        pass
    
    @abstractmethod
    def get_by_profile_id(self, profile_id: int) -> ProfilePermission:
        pass

    @abstractmethod
    def get_by_permission_id(self, permission_id: int) -> ProfilePermission:
        pass

    @abstractmethod
    def get_all(self) -> List[ProfilePermission]:
        pass

    @abstractmethod
    def update(self, profile_permission: ProfilePermission) -> ProfilePermission:
        pass

    @abstractmethod
    def delete(self, profile_permission: ProfilePermission) -> None:
        pass

__all__ = ['IProfilePermissionRepository']
from typing import Optional
from src.core.domain.entities.base_entity import BaseEntity

class Profile(BaseEntity):

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        profile_permissions: Optional[list] = [],
        permissions: Optional[list] = [],
        user_profiles: Optional[list] = [],
        users: Optional[list] = [],
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._name = name
        self._description = description
        self._profile_permissions = profile_permissions
        self._permissions = permissions
        self._user_profiles = user_profiles
        self._users = users
        
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        if not value.strip():
            raise ValueError("Description cannot be empty")
        self._description = value

    @property
    def profile_permissions(self) -> list:
        return self._profile_permissions
    
    @profile_permissions.setter
    def profile_permissions(self, value: list):
        if not isinstance(value, list):
            raise ValueError("Profile permissions must be a list")
        self._profile_permissions = value

    @property
    def permissions(self) -> list:
        return self._permissions
    
    @permissions.setter
    def permissions(self, value: list):
        if not isinstance(value, list):
            raise ValueError("Permissions must be a list")
        self._permissions = value

    @property
    def user_profiles(self) -> list:
        return self._user_profiles
    
    @user_profiles.setter
    def user_profiles(self, value: list):
        if not isinstance(value, list):
            raise ValueError("User profiles must be a list")
        self._user_profiles = value

    @property
    def users(self) -> list:
        return self._users
    
    @users.setter
    def users(self, value: list):
        if not isinstance(value, list):
            raise ValueError("Users must be a list")
        self._users = value

__all__ = ["Profile"]

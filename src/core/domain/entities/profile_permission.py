from datetime import datetime
from typing import Optional
from src.core.domain.entities.permission import Permission
from src.core.domain.entities.profile import Profile
from src.core.domain.entities.base_entity import BaseEntity


class ProfilePermission(BaseEntity):
    
    def __init__(
        self,
        profile: Profile,
        permission: Permission,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._profile = profile
        self._permission = permission
        
    @property
    def profile(self) -> Profile:
        return self._profile
    
    @profile.setter
    def profile(self, profile: Profile):
        self._profile = profile
    
    @property
    def permission(self) -> Permission:
        return self._permission
    
    @permission.setter
    def permission(self, permission: Permission):
        self._permission = permission

__all__ = ['ProfilePermission']

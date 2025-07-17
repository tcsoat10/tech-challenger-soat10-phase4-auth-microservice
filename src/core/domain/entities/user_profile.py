from datetime import datetime
from typing import Optional
from src.core.domain.entities.base_entity import BaseEntity


class UserProfile(BaseEntity):
    
    def __init__(
        self,
        user,
        profile,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None,
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._user = user
        self._profile = profile
        
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        self._user = value
        
    @property
    def profile(self):
        return self._profile
    
    @profile.setter
    def profile(self, value):
        self._profile = value

__all__ = ["UserProfile"]

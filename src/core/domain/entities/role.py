from datetime import datetime
from typing import Optional
from src.core.domain.entities.base_entity import BaseEntity


class Role(BaseEntity):

    def __init__(
        self,
        name: str,
        description: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._name = name
        self._description = description
        
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value

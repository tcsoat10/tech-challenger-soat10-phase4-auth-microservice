from src.core.domain.entities.person import Person
from src.core.domain.entities.base_entity import BaseEntity
from typing import Optional


class Customer(BaseEntity):
    def __init__(
        self,
        person: Person,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self.person: Person = person


__all__ = ['Customer']

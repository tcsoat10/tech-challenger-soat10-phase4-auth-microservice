from datetime import datetime
from typing import Optional
from src.core.domain.entities.person import Person
from src.core.domain.entities.role import Role
from src.core.domain.entities.user import User
from src.core.domain.entities.base_entity import BaseEntity


class Employee(BaseEntity):
    
    def __init__(
        self,
        person: Person,
        role: Role,
        user: User,
        admission_date: Optional[datetime] = None,
        termination_date: Optional[datetime] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None,
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._admission_date = admission_date
        self._termination_date = termination_date
        self._person = person
        self._role = role
        self._user = user
    
    @property
    def admission_date(self) -> datetime:
        return self._admission_date
    
    @admission_date.setter
    def admission_date(self, value: datetime):
        self._admission_date = value

    @property
    def termination_date(self) -> datetime:
        return self._termination_date
    
    @termination_date.setter
    def termination_date(self, value: datetime):
        self._termination_date = value

    @property
    def person(self) -> Person:
        return self._person
    
    @person.setter
    def person(self, value: Person):
        self._person = value

    @property
    def role(self) -> Role:
        return self._role
    
    @role.setter
    def role(self, value: Role):
        self._role = value

    @property
    def user(self) -> User:
        return self._user
    
    @user.setter
    def user(self, value: User):
        self._user = value
    


__all__ = ['Employee']

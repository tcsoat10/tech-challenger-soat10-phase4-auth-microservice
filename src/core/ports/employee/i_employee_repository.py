from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.employee import Employee


class IEmployeeRepository(ABC):
    @abstractmethod
    def create(self, employee: Employee) -> Employee:
        pass

    def get_by_id(self, employee_id: int) -> Employee:
        pass

    def get_by_person_id(self, person_id: int) -> Employee:
        pass

    def get_by_user_id(self, user_id: int) -> Employee:
        pass

    def get_by_role_id(self, role_id: int) -> List[Employee]:
        pass

    def get_by_username(self, username: str) -> Employee:
        pass

    def get_all(self) -> List[Employee]:
        pass

    def update(self, employee: Employee) -> Employee:
        pass

    def delete(self, employee_id: int) -> Employee:
        pass
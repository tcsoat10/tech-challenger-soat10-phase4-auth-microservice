from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.person import Person


class IPersonRepository(ABC):
    
    @abstractmethod
    def create(person: Person):
        pass

    @abstractmethod
    def exists_by_cpf(self, cpf: str) -> bool:
        pass

    @abstractmethod
    def exists_by_email(self, cpf: str) -> bool:
        pass

    @abstractmethod
    def get_by_cpf(self, cpf: str) -> Person:
        pass

    @abstractmethod
    def get_by_id(self, person_id: int) -> Person:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Person]:
        pass

    @abstractmethod
    def update(self, person: Person) -> Person:
        pass

    @abstractmethod
    def delete(self, person_id: int) -> None:
        pass

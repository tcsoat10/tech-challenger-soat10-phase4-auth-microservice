from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.customer import Customer


class ICustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Customer:
        pass

    def get_by_cpf(self, cpf: str) -> Customer:
        pass

    @abstractmethod
    def get_by_person_id(self, person_id: int) -> Customer:
        pass

    @abstractmethod
    def get_all(self) -> List[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def delete(self, customer: Customer) -> None:
        pass
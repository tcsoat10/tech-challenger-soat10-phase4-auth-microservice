from datetime import datetime
from src.core.domain.entities.base_entity import BaseEntity
from pycpfcnpj import cpfcnpj
from typing import Optional


class Person(BaseEntity):
    
    def __init__(
        self,
        name: str,
        cpf: Optional[str] = None,
        email: Optional[str] = None,
        birth_date: Optional[datetime] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._name: str = name
        self._cpf: str = cpf
        self._email: str = email
        self._birth_date: str = birth_date
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = name
        
    @property
    def cpf(self) -> str:
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf: str) -> None:
        if not cpfcnpj.validate(cpf):
            raise ValueError("Invalid CPF")

        self._cpf = cpf
        
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email: str) -> None:
        self._email = email
        
    @property
    def birth_date(self) -> str:
        return self._birth_date
    
    @birth_date.setter
    def birth_date(self, birth_date: str) -> None:
        self._birth_date = birth_date
        
    
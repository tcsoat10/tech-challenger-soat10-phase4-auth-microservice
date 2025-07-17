from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from src.core.domain.entities.person import Person
from pycpfcnpj import cpfcnpj


class PersonDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    cpf: Optional[str] = Field(
        None,
        min_length=11,
        max_length=11,
        pattern=r"^\d{11}$",
        description="CPF deve conter exatamente 11 dígitos numéricos."
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Nome deve ter entre 3 e 200 caracteres."
    )
    email: Optional[EmailStr] = Field(
        None,
        min_length=3,
        max_length=150,
        description="E-mail válido com formato correto."
    )
    birth_date: Optional[date] = Field(
        None, 
        description="Data de nascimento no formato YYYY-MM-DD."
    )

    @field_validator("cpf")
    def validate_cpf(cls, cpf: Optional[str]) -> Optional[str]:
        if cpf and not cpfcnpj.cpf.validate(cpf):
            raise ValueError("CPF inválido.")
        return cpf

    @classmethod
    def from_entity(cls, person: Person) -> "PersonDTO":
        """
        Converte a entidade de domínio `Person` para o DTO.
        """
        return cls(
            id=person.id,
            cpf=person.cpf,
            name=person.name,
            email=person.email,
            birth_date=person.birth_date
        )

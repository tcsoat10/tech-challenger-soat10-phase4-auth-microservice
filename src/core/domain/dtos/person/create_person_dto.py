from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pycpfcnpj import cpfcnpj

class CreatePersonDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    cpf: str = Field(
        ...,
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
    email: EmailStr = Field(
        ...,
        min_length=3,
        max_length=150,
        description="E-mail válido com formato correto."
    )
    birth_date: date = Field(
        ..., 
        description="Data de nascimento no formato YYYY-MM-DD."
    )
    
    @field_validator('cpf')
    def cpf_must_be_valid(cls, cpf):
        if cpf and not cpfcnpj.cpf.validate(cpf):
            raise ValueError("CPF inválido.")
        return cpf

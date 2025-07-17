from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class UpdatePersonDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    cpf: str = Field(..., min_length=11, max_length=11)
    name: str = Field(..., min_length=3, max_length=200)
    email: str = Field(..., min_length=3, max_length=150)
    birth_date: date
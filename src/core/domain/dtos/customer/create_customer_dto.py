from pydantic import BaseModel, ConfigDict, Field
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO


class CreateCustomerDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    person: CreatePersonDTO

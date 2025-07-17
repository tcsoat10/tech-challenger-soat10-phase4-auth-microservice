from pydantic import BaseModel, ConfigDict

from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO


class UpdateCustomerDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    person: CreatePersonDTO
from pydantic import BaseModel, ConfigDict, Field

from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO


class CreateEmployeeDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    role_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    person: CreatePersonDTO
    
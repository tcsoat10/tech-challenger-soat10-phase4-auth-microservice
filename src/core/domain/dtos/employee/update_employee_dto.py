from pydantic import BaseModel, ConfigDict, Field


class UpdateEmployeeDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    person_id: int = Field(..., gt=0)
    role_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    
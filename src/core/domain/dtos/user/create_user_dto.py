from pydantic import BaseModel, ConfigDict, Field


class CreateUserDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    name: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=50)

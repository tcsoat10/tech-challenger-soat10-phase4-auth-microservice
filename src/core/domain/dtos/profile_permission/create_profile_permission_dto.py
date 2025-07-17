from pydantic import BaseModel, ConfigDict, Field


class CreateProfilePermissionDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    permission_id: int = Field(..., gt=0)
    profile_id: int = Field(..., gt=0)
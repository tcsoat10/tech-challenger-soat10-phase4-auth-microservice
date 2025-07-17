from pydantic import BaseModel, ConfigDict, Field


class UpdateProfilePermissionDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    permission_id: int = Field(..., gt=0)
    profile_id: int = Field(..., gt=0)
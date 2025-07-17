
from pydantic import BaseModel, ConfigDict, Field


class CreateUserProfileDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    user_id: int = Field(..., gt=0, description='User ID')
    profile_id: int = Field(..., gt=0, description='Profile ID')

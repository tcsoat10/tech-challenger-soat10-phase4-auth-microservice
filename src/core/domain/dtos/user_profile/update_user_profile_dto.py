
from pydantic import BaseModel, ConfigDict, Field


class UpdateUserProfileDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int = Field(..., gt=0, description='User Profile ID')
    user_id: int = Field(..., gt=0, description='User ID')
    profile_id: int = Field(..., gt=0, description='Profile ID')

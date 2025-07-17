from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class CreateOrderDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id_customer: Optional[int] = Field(..., gt=0)

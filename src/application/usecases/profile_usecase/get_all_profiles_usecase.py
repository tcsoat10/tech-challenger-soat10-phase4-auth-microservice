from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.entities.profile import Profile

from typing import Optional, List


class GetAllProfilesUsecase:
    def __init__(self, profile_gateway: IProfileRepository):
        self.profile_gateway = profile_gateway

    @classmethod
    def build(cls, profile_gateway: IProfileRepository):
        return cls(profile_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[Profile]:
        profiles = self.profile_gateway.get_all(include_deleted=include_deleted)
        return profiles
from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.domain.entities.user_profile import UserProfile

from typing import Optional, List


class GetAllUserProfilesUsecase:
    def __init__(self, user_profile_gateway: IUserProfileRepository):
        self.user_profile_gateway = user_profile_gateway

    @classmethod
    def build(cls, user_profile_gateway: IUserProfileRepository) -> 'GetAllUserProfilesUsecase':
        return cls(user_profile_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[UserProfile]:
        user_profiles = self.user_profile_gateway.get_all(include_deleted)
        return user_profiles

from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.domain.entities.user_profile import UserProfile
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class GetUserProfileByUserIdAndProfileIdUsecase:
    def __init__(self, user_profile_gateway: IUserProfileRepository):
        self.user_profile_gateway = user_profile_gateway

    @classmethod
    def build(cls, user_profile_gateway: IUserProfileRepository) -> 'GetUserProfileByUserIdAndProfileIdUsecase':
        return cls(user_profile_gateway)
    
    def execute(self, user_id: int, profile_id: int):
        user_profile = self.user_profile_gateway.get_by_user_id_and_profile_id(user_id, profile_id)
        if not user_profile:
            raise EntityNotFoundException('UserProfile')
        return user_profile
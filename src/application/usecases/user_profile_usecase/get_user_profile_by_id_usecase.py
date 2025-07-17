from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.domain.entities.user_profile import UserProfile
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class GetUserProfileByIdUsecase:
    def __init__(self, user_profile_gateway: IUserProfileRepository):
        self.user_profile_gateway = user_profile_gateway
    
    @classmethod
    def build(cls, user_profile_gateway: IUserProfileRepository) -> 'GetUserProfileByIdUsecase':
        return cls(user_profile_gateway)
    
    def execute(self, user_profile_id: int) -> UserProfile:
        user_profile = self.user_profile_gateway.get_by_id(user_profile_id)
        if not user_profile:
            raise EntityNotFoundException(entity_name='UserProfile')
        return user_profile
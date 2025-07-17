from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user_profile.update_user_profile_dto import UpdateUserProfileDTO
from src.core.domain.entities.user_profile import UserProfile
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class UpdateUserProfileUsecase:
    def __init__(
            self,
            user_profile_gateway: IUserProfileRepository,
            profile_gateway: IProfileRepository,
            user_gateway: IUserRepository
    ):
        self.user_profile_gateway = user_profile_gateway
        self.profile_gateway = profile_gateway
        self.user_gateway = user_gateway

    @classmethod
    def build(
        cls,
        user_profile_gateway: IUserProfileRepository,
        profile_gateway: IProfileRepository,
        user_gateway: IUserRepository
    ) -> 'UpdateUserProfileUsecase':
        return cls(user_profile_gateway, profile_gateway, user_gateway)
    
    def execute(self, user_profile_id: int, dto: UpdateUserProfileDTO) -> UserProfile:
        user_profile = self.user_profile_gateway.get_by_id(user_profile_id)
        if not user_profile:
            raise EntityNotFoundException(entity_name='UserProfile')
        
        profile = self.profile_gateway.get_by_id(dto.profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        
        user = self.user_gateway.get_by_id(dto.user_id)
        if not user:
            raise EntityNotFoundException(entity_name='User')
        
        user_profile.profile = profile
        user_profile.user = user

        user_profile = self.user_profile_gateway.update(user_profile)
        return user_profile

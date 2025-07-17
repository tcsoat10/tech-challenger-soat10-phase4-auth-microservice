from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.entities.user_profile import UserProfile
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException


class CreateUserProfileUsecase:
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
    ) -> 'CreateUserProfileUsecase':
        return cls(user_profile_gateway, profile_gateway, user_gateway)
    
    def execute(self, dto: CreateUserProfileDTO) -> UserProfile:
        user = self.user_gateway.get_by_id(dto.user_id)
        if not user:
            raise EntityNotFoundException(entity_name='User')

        profile = self.profile_gateway.get_by_id(dto.profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')        
        
        
        user_profile = self.user_profile_gateway.get_by_user_id_and_profile_id(dto.user_id, dto.profile_id)
        if user_profile:
            if not user_profile.is_deleted():
                raise EntityDuplicatedException(entity_name='User Profile')
            
            user_profile.profile = profile
            user_profile.user = user
            user_profile.reactivate()
            self.user_profile_gateway.update(user_profile)
        else:
            user_profile = UserProfile(profile=profile, user=user)
            user_profile = self.user_profile_gateway.create(user_profile)
        
        return user_profile


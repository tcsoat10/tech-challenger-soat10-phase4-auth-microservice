from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeleteUserProfileUsecase:
    def __init__(self, user_profile_gateway: IUserProfileRepository):
        self.user_profile_gateway = user_profile_gateway

    @classmethod
    def build(cls, user_profile_gateway: IUserProfileRepository) -> 'DeleteUserProfileUsecase':
        return cls(user_profile_gateway)
    
    def execute(self, user_profile_id: int) -> None:
        user_profile = self.user_profile_gateway.get_by_id(user_profile_id)
        if not user_profile:
            raise EntityNotFoundException(entity_name='UserProfile')
        
        if DELETE_MODE == 'soft':
            if user_profile.is_deleted():
                raise EntityNotFoundException(entity_name='UserProfile')
            
            user_profile.soft_delete()
            self.user_profile_gateway.update(user_profile)
        else:
            self.user_profile_gateway.delete(user_profile)
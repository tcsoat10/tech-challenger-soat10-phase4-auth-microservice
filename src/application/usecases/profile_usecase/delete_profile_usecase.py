from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeleteProfileUsecase:
    def __init__(self, profile_gateway: IProfileRepository):
        self.profile_gateway = profile_gateway

    @classmethod
    def build(cls, profile_gateway: IProfileRepository) -> 'DeleteProfileUsecase':
        return cls(profile_gateway)
    
    def execute(self, profile_id: int) -> None:
        profile = self.profile_gateway.get_by_id(profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        
        if DELETE_MODE == 'soft':
            if profile.is_deleted():
                raise EntityNotFoundException(entity_name='Profile')
            
            profile.soft_delete()
            self.profile_gateway.update(profile)
        else:
            self.profile_gateway.delete(profile)
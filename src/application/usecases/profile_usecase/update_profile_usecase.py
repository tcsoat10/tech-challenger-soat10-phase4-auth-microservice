from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.dtos.profile.update_profile_dto import UpdateProfileDTO
from src.core.domain.entities.profile import Profile
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class UpdateProfileUsecase:
    def __init__(self, profile_gateway: IProfileRepository):
        self.profile_gateway = profile_gateway

    @classmethod
    def build(cls, profile_gateway: IProfileRepository) -> 'UpdateProfileUsecase':
        return cls(profile_gateway)
    
    def execute(self, profile_id: int, dto: UpdateProfileDTO) -> Profile:
        profile = self.profile_gateway.get_by_id(profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        
        profile.name = dto.name
        profile.description = dto.description
        updated_profile = self.profile_gateway.update(profile)

        return updated_profile
    
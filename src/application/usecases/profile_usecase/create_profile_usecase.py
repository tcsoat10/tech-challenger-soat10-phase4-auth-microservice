from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.domain.entities.profile import Profile
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException


class CreateProfileUsecase:
    def __init__(self, profile_gateway: IProfileRepository):
        self.profile_gateway = profile_gateway

    @classmethod
    def build(cls, profile_gateway: IProfileRepository):
        return cls(profile_gateway)
    
    def execute(self, dto: CreateProfileDTO) -> Profile:
        profile = self.profile_gateway.get_by_name(dto.name)
        if profile:
            if not profile.is_deleted():
                raise EntityDuplicatedException(entity_name='Profile')
            
            profile.name = dto.name
            profile.description = dto.description
            profile.reactivate()
            self.profile_gateway.update(profile)

        else:
            profile = Profile(name=dto.name, description=dto.description)
            profile = self.profile_gateway.create(profile)

        return profile
    
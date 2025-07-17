from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class GetProfilePermissionByIdUsecase:
    def __init__(self, profile_permission_gateway: IProfilePermissionRepository):
        self.profile_permission_gateway = profile_permission_gateway

    @classmethod
    def build(cls, profile_permission_gateway: IProfilePermissionRepository):
        return cls(profile_permission_gateway)
    
    def execute(self, profile_permission_id: int) -> ProfilePermissionDTO:
        profile_permission = self.profile_permission_gateway.get_by_id(profile_permission_id)
        if not profile_permission:
            raise EntityNotFoundException(entity_name='Profile Permission')
        
        return profile_permission
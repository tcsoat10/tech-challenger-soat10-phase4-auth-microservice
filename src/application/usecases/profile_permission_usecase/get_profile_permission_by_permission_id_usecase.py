from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.domain.entities.profile_permission import ProfilePermission
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class GetProfilePermissionByPermissionIdUsecase:
    def __init__(self, profile_permission_gateway: IProfilePermissionRepository):
        self.profile_permission_gateway = profile_permission_gateway
    
    @classmethod
    def build(
        cls, profile_permission_gateway: IProfilePermissionRepository
    ) -> 'GetProfilePermissionByPermissionIdUsecase':
        return cls(profile_permission_gateway)
    
    def execute(self, permission_id) -> ProfilePermission:
        profile_permission = self.profile_permission_gateway.get_by_permission_id(permission_id)
        if not profile_permission:
            raise EntityNotFoundException(entity_name='Profile Permission')
        return profile_permission
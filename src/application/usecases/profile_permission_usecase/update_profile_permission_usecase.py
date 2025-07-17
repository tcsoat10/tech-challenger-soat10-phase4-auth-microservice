from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.dtos.profile_permission.update_profile_permission_dto import UpdateProfilePermissionDTO
from src.core.domain.entities.profile_permission import ProfilePermission
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException



class UpdateProfilePermissionUsecase:
    def __init__(
            self,
            profile_permission_gateway: IProfilePermissionRepository,
            permission_gateway: IPermissionRepository,
            profile_gateway: IProfileRepository
    ):
        self.profile_permission_gateway = profile_permission_gateway
        self.permission_gateway = permission_gateway
        self.profile_gateway = profile_gateway

    @classmethod
    def build(
        cls,
        profile_permission_gateway: IProfilePermissionRepository,
        permission_gateway: IPermissionRepository,
        profile_gateway: IProfileRepository
    ) -> 'UpdateProfilePermissionUsecase':
        return cls(profile_permission_gateway, permission_gateway, profile_gateway)
    
    def execute(self, profile_permission_id: int, dto: UpdateProfilePermissionDTO) -> ProfilePermission:
        profile_permission = self.profile_permission_gateway.get_by_id(profile_permission_id)
        if not profile_permission:
            raise EntityNotFoundException(entity_name='Profile Permission')
        
        permission = self.permission_gateway.get_by_id(dto.permission_id)
        if not permission:
            raise EntityNotFoundException(entity_name='Permission')
        
        profile = self.profile_gateway.get_by_id(dto.profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        
        profile_permission.permission = permission
        profile_permission.profile = profile

        profile_permission = self.profile_permission_gateway.update(profile_permission)
        return profile_permission
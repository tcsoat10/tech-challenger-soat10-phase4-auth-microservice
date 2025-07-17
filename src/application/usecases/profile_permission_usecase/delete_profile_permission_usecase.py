from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeleteProfilePermissionUsecase:
    def __init__(self, profile_permission_gateway: IProfilePermissionRepository):
        self.profile_permission_gateway = profile_permission_gateway

    @classmethod
    def build(cls, profile_permission_gateway: IProfilePermissionRepository) -> 'DeleteProfilePermissionUsecase':
        return cls(profile_permission_gateway)
    
    def execute(self, profile_permission_id: int) -> None:
        profile_permission = self.profile_permission_gateway.get_by_id(profile_permission_id)
        if not profile_permission:
            raise EntityNotFoundException(entity_name='Profile Permission')
        
        if DELETE_MODE == 'soft':
            if profile_permission.is_deleted():
                raise EntityNotFoundException(entity_name='Profile Permission')
            
            profile_permission.soft_delete()
            self.profile_permission_gateway.update(profile_permission)
        else:
            self.profile_permission_gateway.delete(profile_permission)
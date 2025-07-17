from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeletePermissionUsecase:
    def __init__(self, permission_gateway: IPermissionRepository):
        self.permission_gateway = permission_gateway

    @classmethod
    def build(cls, permission_gateway: IPermissionRepository) -> 'DeletePermissionUsecase':
        return cls(permission_gateway)
    
    def execute(self, permission_id: int) -> None:
        permission = self.permission_gateway.get_by_id(permission_id)
        if not permission:
            raise EntityNotFoundException(entity_name='Permission')
        
        if DELETE_MODE == 'soft':
            if permission.is_deleted():
                raise EntityNotFoundException(entity_name='Permission')
            
            permission.soft_delete()
            self.permission_gateway.update(permission)
        else:
            self.permission_gateway.delete(permission)
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.domain.entities.permission import Permission
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class GetPermissionByIdUsecase:
    def __init__(self, permission_gateway: IPermissionRepository):
        self.permission_gateway = permission_gateway

    @classmethod
    def build(cls, permission_gateway: IPermissionRepository):
        return cls(permission_gateway)
    
    def execute(self, permission_id: int) -> Permission:
        permission = self.permission_gateway.get_by_id(permission_id)
        if not permission:
            raise EntityNotFoundException(entity_name='Permission')
        
        return permission
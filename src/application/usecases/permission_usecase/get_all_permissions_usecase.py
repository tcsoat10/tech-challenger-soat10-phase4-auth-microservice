from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.domain.entities.permission import Permission

from typing import Optional, List


class GetAllPermissionsUsecase:
    def __init__(self, permission_gateway: IPermissionRepository):
        self.permission_gateway = permission_gateway

    @classmethod
    def build(cls, permission_gateway: IPermissionRepository):
        return cls(permission_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[Permission]:
        permissions = self.permission_gateway.get_all(include_deleted=include_deleted)
        return permissions
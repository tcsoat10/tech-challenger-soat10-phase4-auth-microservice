from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO

from typing import Optional


class GetAllProfilePermissionsUsecase:
    def __init__(self, profile_permission_gateway: IProfilePermissionRepository):
        self.profile_permission_gateway = profile_permission_gateway

    @classmethod
    def build(cls, profile_permission_gateway: IProfilePermissionRepository) -> 'GetAllProfilePermissionsUsecase':
        return cls(profile_permission_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> ProfilePermissionDTO:
        profile_permissions = self.profile_permission_gateway.get_all(include_deleted)
        return profile_permissions

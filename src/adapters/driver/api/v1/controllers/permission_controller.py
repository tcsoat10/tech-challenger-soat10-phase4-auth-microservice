from typing import Optional, List

from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.application.usecases.permission_usecase.create_permission_usecase import CreatePermissionUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.permission_usecase.get_permission_by_name_usecase import GetPermissionByNameUseCase
from src.application.usecases.permission_usecase.get_permission_by_id_usecase import GetPermissionByIdUsecase
from src.application.usecases.permission_usecase.get_all_permissions_usecase import GetAllPermissionsUsecase
from src.application.usecases.permission_usecase.update_permission_usecase import UpdatePermissionUsecase
from src.application.usecases.permission_usecase.delete_permission_usecase import DeletePermissionUsecase


class PermissionController:

    def __init__(self, permission_gateway: IPermissionRepository):
        self.permission_gateway: IPermissionRepository = permission_gateway
    
    def create_permission(self, dto: CreatePermissionDTO) -> PermissionDTO:
        create_permission_usecase = CreatePermissionUsecase.build(self.permission_gateway)
        permission = create_permission_usecase.execute(dto)
        return DTOPresenter.transform(permission, PermissionDTO)
    
    def get_permission_by_name(self, name: str) -> PermissionDTO:
        permission_by_name_usecase = GetPermissionByNameUseCase.build(self.permission_gateway)
        permission = permission_by_name_usecase.execute(name)
        return DTOPresenter.transform(permission, PermissionDTO)
    
    def get_permission_by_id(self, permission_id: int) -> PermissionDTO:
        permission_by_id_usecase = GetPermissionByIdUsecase.build(self.permission_gateway)
        permission = permission_by_id_usecase.execute(permission_id)
        return DTOPresenter.transform(permission, PermissionDTO)
    
    def get_all_permissions(self, include_deleted: Optional[bool]) -> List[PermissionDTO]:
        all_permissions_usecase = GetAllPermissionsUsecase.build(self.permission_gateway)
        permissions = all_permissions_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(permissions, PermissionDTO)
    
    def update_permission(self, permission_id: int, dto: CreatePermissionDTO) -> PermissionDTO:
        update_permission_usecase = UpdatePermissionUsecase.build(self.permission_gateway)
        permission = update_permission_usecase.execute(permission_id, dto)
        return DTOPresenter.transform(permission, PermissionDTO)
    
    def delete_permission(self, permission_id: int) -> None:
        delete_permission_usecase = DeletePermissionUsecase.build(self.permission_gateway)
        delete_permission_usecase.execute(permission_id)
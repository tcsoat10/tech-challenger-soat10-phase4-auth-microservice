from typing import Optional, List

from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.dtos.profile_permission.create_profile_permission_dto import CreateProfilePermissionDTO
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO
from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.application.usecases.profile_permission_usecase.create_profile_permission_usecase import CreateProfilePermissionUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.profile_permission_usecase.get_profile_permission_by_id_usecase import GetProfilePermissionByIdUsecase
from src.application.usecases.profile_permission_usecase.get_profile_permission_by_permission_id_usecase import GetProfilePermissionByPermissionIdUsecase
from src.application.usecases.profile_permission_usecase.get_profile_permission_by_profile_id_usecase import GetProfilePermissionByProfileIdUsecase
from src.application.usecases.profile_permission_usecase.get_all_profile_permissions_usecase import GetAllProfilePermissionsUsecase
from src.core.domain.dtos.profile_permission.update_profile_permission_dto import UpdateProfilePermissionDTO
from src.application.usecases.profile_permission_usecase.update_profile_permission_usecase import UpdateProfilePermissionUsecase
from src.application.usecases.profile_permission_usecase.delete_profile_permission_usecase import DeleteProfilePermissionUsecase


class ProfilePermissionController:
    
    def __init__(
        self,
        profile_permission_gateway: IProfilePermissionRepository,
        permission_gateway: IPermissionRepository,
        profile_gateway: IProfileRepository
    ) -> None:
        self.profile_permission_gateway: IProfilePermissionRepository = profile_permission_gateway
        self.permission_gateway: IPermissionRepository = permission_gateway
        self.profile_gateway: IProfileRepository = profile_gateway
        
    
    def create_profile_permission(self, dto: CreateProfilePermissionDTO) -> ProfilePermissionDTO:
        create_profile_permission_usecase = CreateProfilePermissionUsecase.build(
            self.profile_permission_gateway, self.permission_gateway, self.profile_gateway
        )
        profile_permission = create_profile_permission_usecase.execute(dto)
        return DTOPresenter.transform(profile_permission, ProfilePermissionDTO)
    
    def get_profile_permission_by_id(self, profile_permission_id: int) -> ProfilePermissionDTO:
        get_profile_permission_by_id_usecase = GetProfilePermissionByIdUsecase.build(self.profile_permission_gateway)
        profile_permission = get_profile_permission_by_id_usecase.execute(profile_permission_id)
        return DTOPresenter.transform(profile_permission, ProfilePermissionDTO)
    
    def get_profile_permission_by_permission_id(self, permission_id: int) -> ProfilePermissionDTO:
        get_profile_permission_by_permission_id_usecase = GetProfilePermissionByPermissionIdUsecase(
            self.profile_permission_gateway
        )
        profile_permission = get_profile_permission_by_permission_id_usecase.execute(permission_id)
        return DTOPresenter.transform(profile_permission, ProfilePermissionDTO)
    
    def get_profile_permission_by_profile_id(self, profile_id: int) -> ProfilePermissionDTO:
        get_profile_permission_by_profile_id_usecase = GetProfilePermissionByProfileIdUsecase(
            self.profile_permission_gateway
        )
        profile_permission = get_profile_permission_by_profile_id_usecase.execute(profile_id)
        return DTOPresenter.transform(profile_permission, ProfilePermissionDTO)
    
    def get_all_profile_permissions(self, include_deleted: Optional[bool] = False) -> List[ProfilePermissionDTO]:
        get_all_profile_permissions_usecase = GetAllProfilePermissionsUsecase.build(self.profile_permission_gateway)
        profile_permissions = get_all_profile_permissions_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(profile_permissions, ProfilePermissionDTO)
    
    def update_profile_permission(
            self, profile_permission_id: int, dto: UpdateProfilePermissionDTO
    ) -> ProfilePermissionDTO:
        update_profile_permission_usecase = UpdateProfilePermissionUsecase.build(
            self.profile_permission_gateway, self.permission_gateway, self.profile_gateway
        )
        profile_permission = update_profile_permission_usecase.execute(profile_permission_id, dto)
        return DTOPresenter.transform(profile_permission, ProfilePermissionDTO)
    
    def delete_profile_permission(self, profile_permission_id: int) -> None:
        delete_profile_permission_usecase = DeleteProfilePermissionUsecase.build(self.profile_permission_gateway)
        delete_profile_permission_usecase.execute(profile_permission_id)
from typing import List, Optional

from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.application.usecases.role_usecase.create_role_usecase import CreateRoleUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.role_usecase.get_role_by_name_usecase import GetRoleByNameUsecase
from src.application.usecases.role_usecase.get_role_by_id_usecase import GetRoleByIdUsecase
from src.application.usecases.role_usecase.get_all_roles_usecase import GetAllRolesUsecase
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO
from src.application.usecases.role_usecase.update_role_usecase import UpdateRoleUsecase
from src.application.usecases.role_usecase.delete_role_usecase import DeleteRoleUsecase


class RoleController:
    
    def __init__(self, role_gateway: IRoleRepository):
        self.role_gateway: IRoleRepository = role_gateway

    def create_role(self, dto: CreateRoleDTO) -> RoleDTO:
        create_role_usecase = CreateRoleUsecase.build(self.role_gateway)
        role = create_role_usecase.execute(dto)
        return DTOPresenter.transform(role, RoleDTO)
    
    def get_role_by_name(self, name: str) -> RoleDTO:
        role_by_name_usecase = GetRoleByNameUsecase.build(self.role_gateway)
        role = role_by_name_usecase.exexute(name)
        return DTOPresenter.transform(role, RoleDTO)
    
    def get_role_by_id(self, role_id: int) -> RoleDTO:
        role_by_id_usecase = GetRoleByIdUsecase.build(self.role_gateway)
        role = role_by_id_usecase.exexute(role_id)
        return DTOPresenter.transform(role, RoleDTO)
    
    def get_all_roles(self, include_deleted: Optional[bool] = False) -> List[RoleDTO]:
        all_roles_usecase = GetAllRolesUsecase.build(self.role_gateway)
        roles = all_roles_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(roles, RoleDTO)
    
    def update_role(self, role_id: int, dto: UpdateRoleDTO) -> RoleDTO:
        update_role_usecase = UpdateRoleUsecase.build(self.role_gateway)
        role = update_role_usecase.execute(role_id, dto)
        return DTOPresenter.transform(role, RoleDTO)
    
    def delete_role(self, role_id: int) -> None:
        delete_role_usecase = DeleteRoleUsecase.build(self.role_gateway)
        delete_role_usecase.execute(role_id)
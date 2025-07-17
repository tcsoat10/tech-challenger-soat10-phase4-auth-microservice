from fastapi import APIRouter, Depends, Security, status, Query
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from src.core.auth.dependencies import get_current_user
from src.constants.permissions import RolePermissions
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO
from src.adapters.driver.api.v1.controllers.role_controller import RoleController
from src.core.containers import Container


router = APIRouter()


@router.post(
    '/roles',
    response_model=RoleDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_CREATE_ROLE])],
    include_in_schema=False
)
@inject
def create_role(
    dto: CreateRoleDTO,
    controller: RoleController = Depends(Provide[Container.role_controller]),
    user=Depends(get_current_user)
):
    return controller.create_role(dto)


@router.get(
    '/roles/{role_name}/name',
    response_model=RoleDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_VIEW_ROLES])]
)
@inject
def get_role_by_name(
    role_name: str,
    controller: RoleController = Depends(Provide[Container.role_controller]),
    user=Depends(get_current_user)
):
    return controller.get_role_by_name(role_name)


@router.get(
    '/roles/{role_id}/id',
    response_model=RoleDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_VIEW_ROLES])]
)
@inject
def get_role_by_id(
    role_id: str,
    controller: RoleController = Depends(Provide[Container.role_controller]),
    user=Depends(get_current_user)
):
    return controller.get_role_by_id(role_id)


@router.get(
    '/roles',
    response_model=List[RoleDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_VIEW_ROLES])]
)
@inject
def get_all_roles(
    include_deleted: Optional[bool] = Query(False),
    controller: RoleController = Depends(Provide[Container.role_controller]),
    user=Depends(get_current_user)
):
    return controller.get_all_roles(include_deleted)


@router.put(
    '/roles/{role_id}',
    response_model=RoleDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_UPDATE_ROLE])],
    include_in_schema=False
)
@inject
def update_role(
    role_id: int,
    dto: UpdateRoleDTO,
    controller: RoleController = Depends(Provide[Container.role_controller]),
    user=Depends(get_current_user)
):
    return controller.update_role(role_id, dto)


@router.delete(
    '/roles/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_DELETE_ROLE])],
    include_in_schema=False
)
@inject
def delete_role(
    role_id: int,
    controller: RoleController = Depends(Provide[Container.role_controller]),
    user=Depends(get_current_user)
):
    controller.delete_role(role_id)

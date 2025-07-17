from fastapi import APIRouter, Depends, Security, status, Query
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from src.constants.permissions import PermissionPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.domain.dtos.permission.update_permission_dto import UpdatePermissionDTO
from src.adapters.driver.api.v1.controllers.permission_controller import PermissionController
from src.core.containers import Container


router = APIRouter()


@router.post(
    path='/permissions',
    response_model=PermissionDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_CREATE_PERMISSION])],
    include_in_schema=False
)
@inject
def create_permission(
    dto: CreatePermissionDTO,
    controller: PermissionController = Depends(Provide[Container.permission_controller]),
    user=Depends(get_current_user)
):
    return controller.create_permission(dto)


@router.get(
    path='/permissions/{permission_name}/name',
    response_model=PermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_VIEW_PERMISSIONS])]
)
@inject
def get_permission_by_name(
    permission_name: str,
    controller: PermissionController = Depends(Provide[Container.permission_controller]),
    user=Depends(get_current_user)
):
    return controller.get_permission_by_name(name=permission_name)


@router.get(
    path='/permissions/{permission_id}/id',
    response_model=PermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_VIEW_PERMISSIONS])]
)
@inject
def get_permission_by_id(
    permission_id: int,
    controller: PermissionController = Depends(Provide[Container.permission_controller]),
    user=Depends(get_current_user)
):
    return controller.get_permission_by_id(permission_id)


@router.get(
    path='/permissions',
    response_model=List[PermissionDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_VIEW_PERMISSIONS])]
)
@inject
def get_all_permissions(
    include_deleted: Optional[bool] = Query(False),
    controller: PermissionController = Depends(Provide[Container.permission_controller]),
    user=Depends(get_current_user)
):
    return controller.get_all_permissions(include_deleted)


@router.put(
    path='/permissions/{permission_id}',
    response_model=PermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_UPDATE_PERMISSION])],
    include_in_schema=False
)
@inject
def update_permission(
    permission_id: int,
    dto: UpdatePermissionDTO,
    controller: PermissionController = Depends(Provide[Container.permission_controller]),
    user=Depends(get_current_user)
):
    return controller.update_permission(permission_id, dto)


@router.delete(
    path='/permissions/{permission_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_DELETE_PERMISSION])],
    include_in_schema=False
)
@inject
def delete_permission(
    permission_id: int,
    controller: PermissionController = Depends(Provide[Container.permission_controller]),
    user=Depends(get_current_user)
):
    controller.delete_permission(permission_id)


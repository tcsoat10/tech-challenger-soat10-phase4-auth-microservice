from fastapi import APIRouter, Depends, Security, status
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.profile_permission_controller import ProfilePermissionController
from src.constants.permissions import ProfilePermissionPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO
from src.core.domain.dtos.profile_permission.create_profile_permission_dto import CreateProfilePermissionDTO
from src.core.domain.dtos.profile_permission.update_profile_permission_dto import UpdateProfilePermissionDTO
from src.core.containers import Container


router = APIRouter()


@router.post(
    '/profile_permissions',
    response_model=ProfilePermissionDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissionPermissions.CAN_CREATE_PROFILE_PERMISSION])],
    include_in_schema=False
)
@inject
def create_profile_permission(
    dto: CreateProfilePermissionDTO,
    controller: ProfilePermissionController = Depends(Provide[Container.profile_permission_controller]),
    user=Depends(get_current_user)
):
    return controller.create_profile_permission(dto)


@router.get(
    '/profile_permissions/{profile_permission_id}/id',
    response_model=ProfilePermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])]
)
@inject
def get_profile_permission_by_id(
    profile_permission_id: int,
    controller: ProfilePermissionController = Depends(Provide[Container.profile_permission_controller]),
    user=Depends(get_current_user)
):
    return controller.get_profile_permission_by_id(profile_permission_id)


@router.get(
    '/profile_permissions/{permission_id}/permission_id',
    response_model=ProfilePermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])]
)
@inject
def get_profile_permission_by_permission_id(
    permission_id: int,
    controller: ProfilePermissionController = Depends(Provide[Container.profile_permission_controller]),
    user=Depends(get_current_user)
):
    return controller.get_profile_permission_by_permission_id(permission_id)


@router.get(
    '/profile_permissions/{profile_id}/profile_id',
    response_model=ProfilePermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])]
)
@inject
def get_profile_permission_by_profile_id(
    profile_id: int,
    controller: ProfilePermissionController = Depends(Provide[Container.profile_permission_controller]),
    user=Depends(get_current_user)
):
    return controller.get_profile_permission_by_profile_id(profile_id)


@router.get(
    '/profile_permissions',
    response_model=List[ProfilePermissionDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissionPermissions.CAN_VIEW_PROFILE_PERMISSIONS])]
)
@inject
def get_all_profile_permissions(
    include_deleted: Optional[bool] = False,
    controller: ProfilePermissionController = Depends(Provide[Container.profile_permission_controller]),
    user=Depends(get_current_user)
):
    return controller.get_all_profile_permissions(include_deleted=include_deleted)


@router.put(
    '/profile_permissions/{profile_permission_id}',
    response_model=ProfilePermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissionPermissions.CAN_UPDATE_PROFILE_PERMISSION])],
    include_in_schema=False
)
@inject
def update_profile_permission(
    profile_permission_id: int,
    dto: UpdateProfilePermissionDTO,
    controller: ProfilePermissionController = Depends(Provide[Container.profile_permission_controller]),
    user=Depends(get_current_user)
):
    return controller.update_profile_permission(profile_permission_id, dto)


@router.delete(
    '/profile_permissions/{profile_permission_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissionPermissions.CAN_DELETE_PROFILE_PERMISSION])],
    include_in_schema=False
)
@inject
def delete_profile_permission(
    profile_permission_id: int,
    controller: ProfilePermissionController = Depends(Provide[Container.profile_permission_controller]),
    user=Depends(get_current_user)
):
    controller.delete_profile_permission(profile_permission_id)

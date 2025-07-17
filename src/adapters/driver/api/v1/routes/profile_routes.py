from fastapi import APIRouter, Depends, Query, Security, status
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from src.constants.permissions import ProfilePermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.domain.dtos.profile.update_profile_dto import UpdateProfileDTO
from src.adapters.driver.api.v1.controllers.profile_controller import ProfileController
from src.core.containers import Container


router = APIRouter()


@router.post(
    path='/profiles',
    response_model=ProfileDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_CREATE_PROFILE])],
    include_in_schema=False
)
@inject
def create_profile(
    dto: CreateProfileDTO,
    controller: ProfileController = Depends(Provide[Container.profile_controller]),
    user=Depends(get_current_user)
):
    return controller.create_profile(dto)


@router.get(
    path='/profiles/{profile_name}/name',
    response_model=ProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_VIEW_PROFILES])]
)
@inject
def get_profile_by_name(
    profile_name: str,
    controller: ProfileController = Depends(Provide[Container.profile_controller]),
    user=Depends(get_current_user)
):
    return controller.get_profile_by_name(name=profile_name)


@router.get(
    path='/profiles/{profile_id}/id',
    response_model=ProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_VIEW_PROFILES])]
)
@inject
def get_profile_by_id(
    profile_id: int,
    controller: ProfileController = Depends(Provide[Container.profile_controller]),
    user=Depends(get_current_user)
):
    return controller.get_profile_by_id(profile_id)


@router.get(
    path='/profiles',
    response_model=List[ProfileDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_VIEW_PROFILES])]
)
@inject
def get_all_profiles(
    include_deleted: Optional[bool] = Query(False),
    controller: ProfileController = Depends(Provide[Container.profile_controller]),
    user=Depends(get_current_user)
):
    return controller.get_all_profiles(include_deleted)


@router.put(
    path='/profiles/{profile_id}',
    response_model=ProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_UPDATE_PROFILE])],
    include_in_schema=False
)
@inject
def update_profile(
    profile_id: int,
    dto: UpdateProfileDTO,
    controller: ProfileController = Depends(Provide[Container.profile_controller]),
    user=Depends(get_current_user)
):
    return controller.update_profile(profile_id, dto)


@router.delete(
    path='/profiles/{profile_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_DELETE_PROFILE])],
    include_in_schema=False
)
@inject
def delete_profile(
    profile_id: int,
    controller: ProfileController = Depends(Provide[Container.profile_controller]),
    user=Depends(get_current_user)
):
    controller.delete_profile(profile_id)

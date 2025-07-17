from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Security, status
from dependency_injector.wiring import inject, Provide

from src.constants.permissions import UserProfilePermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.dtos.user_profile.update_user_profile_dto import UpdateUserProfileDTO
from src.core.domain.dtos.user_profile.user_profile_dto import UserProfileDTO
from src.adapters.driver.api.v1.controllers.user_profile_controller import UserProfileController
from src.core.containers import Container


router = APIRouter()


@router.post(
    path='/user-profiles',
    response_model=UserProfileDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_CREATE_USER_PROFILE])]
)
@inject
def create_user_profile(
    dto: CreateUserProfileDTO,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.create_user_profile(dto)

@router.get(
    path='/user-profiles/{id}',
    response_model=UserProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])]
)
@inject
def get_user_profile_by_id(
    id: int,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.get_user_profile_by_id(id)

@router.get(
    path='/user-profiles/{user_id}/{profile_id}',
    response_model=UserProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])]
)
@inject
def get_user_profile_by_user_id_and_profile_id(
    user_id: int,
    profile_id: int,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.get_user_profile_by_user_id_and_profile_id(user_id, profile_id)

@router.get(
    path='/user-profiles',
    response_model=List[UserProfileDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])]
)
@inject
def get_all_user_profiles(
    include_deleted: Optional[bool] = Query(False),
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.get_all_user_profiles(include_deleted=include_deleted)

@router.put(
    path='/user-profiles/{user_profile_id}',
    response_model=UserProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_UPDATE_USER_PROFILE])]
)
@inject
def update_user_profile(
    user_profile_id: int,
    dto: UpdateUserProfileDTO,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.update_user_profile(user_profile_id, dto)

@router.delete(
    path='/user-profiles/{user_profile_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_DELETE_USER_PROFILE])],
    include_in_schema=False
)
@inject
def delete_user_profile(
    user_profile_id: int,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    controller.delete_user_profile(user_profile_id)

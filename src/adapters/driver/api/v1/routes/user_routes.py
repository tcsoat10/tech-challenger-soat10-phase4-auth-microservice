from fastapi import APIRouter, Depends, Security, status
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from src.constants.permissions import UserPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.user.user_dto import UserDTO
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO
from src.adapters.driver.api.v1.controllers.user_controller import UserController
from src.core.containers import Container


router = APIRouter()


@router.post(
    path='/users',
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_CREATE_USER])]
)
@inject
def create_user(
    dto: CreateUserDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
    user: dict = Security(get_current_user)
):
    return controller.create_user(dto)


@router.get(
    path='/users/{user_name}/name',
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_VIEW_USERS])]
)
@inject
def get_user_by_name(
    user_name: str,
    controller: UserController = Depends(Provide[Container.user_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_user_by_name(user_name)


@router.get(
    path='/users/{user_id}/id',
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_VIEW_USERS])]
)
@inject
def get_user_by_id(
    user_id: int,
    controller: UserController = Depends(Provide[Container.user_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_user_by_id(user_id)


@router.get(
    path='/users',
    response_model=List[UserDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_VIEW_USERS])]
)
@inject
def get_all_users(
    include_deleted: Optional[bool] = False,
    controller: UserController = Depends(Provide[Container.user_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_users(include_deleted)


@router.put(
    path='/users/{user_id}',
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_UPDATE_USER])]
)
@inject
def update_user(
    user_id: int,
    dto: UpdateUserDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_user(user_id, dto)


@router.delete(
    path='/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_DELETE_USER])]
)
@inject
def delete_user(
    user_id: int,
    controller: UserController = Depends(Provide[Container.user_controller]),
    user: dict = Security(get_current_user)
):
    controller.delete_user(user_id)
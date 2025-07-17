from fastapi import APIRouter, Depends, status, Security
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.employee_controller import EmployeeController
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import EmployeePermissions
from src.core.containers import Container


router = APIRouter()


@router.post(
        '/employees',
        response_model=EmployeeDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_CREATE_EMPLOYEE])]
)
@inject
def create_employee(
    dto: CreateEmployeeDTO,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.create_employee(dto)


@router.get(
        '/employees/{employee_id}/id',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
@inject
def get_employee_by_id(
    employee_id: int,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_employee_by_id(employee_id)


@router.get(
        '/employees/{person_id}/person_id',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
@inject
def get_employee_by_person_id(
    person_id: int,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_employee_by_person_id(person_id)


@router.get(
        '/employees/{user_id}/user_id',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
@inject
def get_employee_by_user_id(
    user_id: int,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_employee_by_user_id(user_id)


@router.get(
        '/employees/{role_id}/role_id',
        response_model=List[EmployeeDTO],
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
@inject
def list_employees_by_role_id(
    role_id: int,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.list_employees_by_role_id(role_id)


@router.get(
        '/employees',
        response_model=List[EmployeeDTO],
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
@inject
def get_all_employees(
    include_deleted: Optional[bool] = False,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_employees(include_deleted=include_deleted)


@router.put(
        '/employees/{employee_id}',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_UPDATE_EMPLOYEE])]
)
@inject
def update_employee(
    employee_id: int,
    dto: UpdateEmployeeDTO,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_employee(employee_id, dto)


@router.delete(
        '/employees/{employee_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_DELETE_EMPLOYEE])]
)
@inject
def delete_employee(
    employee_id: int,
    controller: EmployeeController = Depends(Provide[Container.employee_controller]),
    user: dict = Security(get_current_user)
):
    return controller.delete_employee(employee_id)
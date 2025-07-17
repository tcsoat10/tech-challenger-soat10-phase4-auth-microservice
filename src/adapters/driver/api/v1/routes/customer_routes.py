from fastapi import APIRouter, Depends, status, Security
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.decorators.bypass_auth import bypass_auth
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import CustomerPermissions
from src.adapters.driver.api.v1.controllers.customer_controller import CustomerController
from src.core.containers import Container


router = APIRouter()


@router.post(
    '/customers',
    response_model=CustomerDTO,
    status_code=status.HTTP_201_CREATED
)
@bypass_auth()
@inject
def create_customer(
    dto: CreateCustomerDTO,
    controller: CustomerController = Depends(Provide[Container.customer_controller]),
):
    return controller.create_customer(dto)


@router.get(
        '/customers/{customer_id}/id',
        response_model=CustomerDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[CustomerPermissions.CAN_VIEW_CUSTOMERS])]
)
@inject
def get_customer_by_id(
    customer_id: int,
    controller: CustomerController = Depends(Provide[Container.customer_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_customer_by_id(customer_id, user)


@router.get(
        '/customers/{person_id}/person_id',
        response_model=CustomerDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[CustomerPermissions.CAN_VIEW_CUSTOMERS])]
)
@inject
def get_customer_by_person_id(
    person_id: int,
    controller: CustomerController = Depends(Provide[Container.customer_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_customer_by_person_id(person_id, user)


@router.get(
        '/customers',
        response_model=List[CustomerDTO],
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[CustomerPermissions.CAN_VIEW_CUSTOMERS])]
)
@inject
def get_all_customers(
    include_deleted: Optional[bool] = False,
    controller: CustomerController = Depends(Provide[Container.customer_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_customers(user, include_deleted=include_deleted)


@router.put(
        '/customers/{customer_id}',
        response_model=CustomerDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[CustomerPermissions.CAN_UPDATE_CUSTOMER])]
)
@inject
def update_customer(
    customer_id: int,
    dto: UpdateCustomerDTO,
    controller: CustomerController = Depends(Provide[Container.customer_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_customer(customer_id, dto, user)


@router.delete(
        '/customers/{customer_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[CustomerPermissions.CAN_DELETE_CUSTOMER])]
)
@inject
def delete_customer(
    customer_id: int,
    controller: CustomerController = Depends(Provide[Container.customer_controller]),
    user: dict = Security(get_current_user)
):
    controller.delete_customer(customer_id, user)
from typing import Optional, List

from src.core.ports.auth.i_auth_provider_gateway import IAuthProviderGateway
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.application.usecases.customer_usecase.create_customer_usecase import CreateCustomerUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.customer_usecase.get_customer_by_id_usecase import GetCustomerByIdUsecase
from src.application.usecases.customer_usecase.get_customer_by_person_id_usecase import GetCustomerByPersonIdUsecase
from src.application.usecases.customer_usecase.get_all_customers_usecase import GetAllCustomersUsecase
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO
from src.application.usecases.customer_usecase.update_customer_usecase import UpdateCustomerUsecase
from src.application.usecases.customer_usecase.delete_customer_usecase import DeleteCustomerUsecase


class CustomerController:
    def __init__(self, customer_gateway: ICustomerRepository, person_gateway: IPersonRepository, auth_provider_gateway: IAuthProviderGateway):
        self.customer_gateway: ICustomerRepository = customer_gateway
        self.person_gateway: IPersonRepository = person_gateway
        self.auth_provider_gateway: IAuthProviderGateway = auth_provider_gateway

    def create_customer(self, dto: CreateCustomerDTO) -> CustomerDTO:
        create_customer_usecase = CreateCustomerUsecase.build(self.customer_gateway, self.person_gateway, self.auth_provider_gateway)
        customer = create_customer_usecase.execute(dto)
        return DTOPresenter.transform(customer, CustomerDTO)
    
    def get_customer_by_id(self, customer_id: int, current_user: dict) -> CustomerDTO:
        customer_by_id_usecase = GetCustomerByIdUsecase.build(self.customer_gateway)
        customer = customer_by_id_usecase.execute(customer_id, current_user)
        return DTOPresenter.transform(customer, CustomerDTO)

    def get_customer_by_person_id(self, person_id: int, current_user: dict) -> CustomerDTO:
        customer_by_person_id_usecase = GetCustomerByPersonIdUsecase.build(self.customer_gateway)
        customer = customer_by_person_id_usecase.execute(person_id, current_user)
        return DTOPresenter.transform(customer, CustomerDTO)
    
    def get_all_customers(self, current_user: dict, include_deleted: Optional[bool] = False) -> List[CustomerDTO]:
        all_customers_usecase = GetAllCustomersUsecase.build(self.customer_gateway)
        customers = all_customers_usecase.execute(current_user, include_deleted)
        return DTOPresenter.transform_list(customers, CustomerDTO)
    
    def update_customer(self, customer_id: int, dto: UpdateCustomerDTO, current_user: dict) -> CustomerDTO:
        update_customer_usecase = UpdateCustomerUsecase.build(self.customer_gateway, self.person_gateway)
        customer = update_customer_usecase.execute(customer_id, dto, current_user)
        return DTOPresenter.transform(customer, CustomerDTO)
    
    def delete_customer(self, customer_id: int, current_user: dict) -> None:
        delete_customer_usecase = DeleteCustomerUsecase.build(self.customer_gateway)
        delete_customer_usecase.execute(customer_id, current_user)
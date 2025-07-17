from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.domain.entities.customer import Customer
from src.application.usecases.customer_usecase.is_customer_usecase import IsCustomerUsecase

from typing import Optional, List


class GetAllCustomersUsecase:
    def __init__(self, customer_gateway: ICustomerRepository):
        self.customer_gateway = customer_gateway

    @classmethod
    def build(cls, customer_gateway: ICustomerRepository) -> 'GetAllCustomers':
        return cls(customer_gateway)
    
    def execute(self, current_user: dict, include_deleted: Optional[bool] = False) -> List[Customer]:
        customers = self.customer_gateway.get_all(include_deleted)

        if IsCustomerUsecase.is_customer(current_user):
            customer = [customer for customer in customers if customer.id == int(current_user['person']['id'])]
        
        return customers

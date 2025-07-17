from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.application.usecases.customer_usecase.is_customer_usecase import IsCustomerUsecase
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeleteCustomerUsecase:
    def __init__(self, customer_gateway: ICustomerRepository):
        self.customer_gateway = customer_gateway

    @classmethod
    def build(cls, customer_gateway: ICustomerRepository) -> 'DeleteCustomerUsecase':
        return cls(customer_gateway)
    
    def execute(self, customer_id: int, current_user) -> None:
        if IsCustomerUsecase.is_customer(current_user) and int(current_user['persno']['id']) != customer_id:
            raise EntityNotFoundException(entity_name='Customer')
        
        customer = self.customer_gateway.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        if customer.is_deleted():
            raise EntityNotFoundException(entity_name='Customer')

        if DELETE_MODE == 'soft':
            customer.soft_delete()
            self.customer_gateway.update(customer)
        else:
            self.customer_gateway.delete(customer)

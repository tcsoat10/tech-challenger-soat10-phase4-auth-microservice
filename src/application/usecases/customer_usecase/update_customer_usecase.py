from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO
from src.core.domain.entities.customer import Customer
from src.application.usecases.customer_usecase.is_customer_usecase import IsCustomerUsecase
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class UpdateCustomerUsecase:
    def __init__(self, customer_gateway: ICustomerRepository, person_gateway: IPersonRepository):
        self.customer_gateway = customer_gateway
        self.person_gateway = person_gateway

    @classmethod
    def build(
        cls,
        customer_gateway: ICustomerRepository,
        person_gateway: IPersonRepository
    ) -> 'UpdateCustomerUsecase':
        return cls(customer_gateway, person_gateway)
    
    def execute(self, customer_id: int, dto: UpdateCustomerDTO, current_user: dict) -> Customer:
        if IsCustomerUsecase.is_customer(current_user) and int(current_user['person']['id']) != customer_id:
            raise EntityNotFoundException(entity_name='Customer')

        customer = self.customer_gateway.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        
        if customer.is_deleted():
            raise EntityNotFoundException(entity_name='Customer')
        
        if customer.person.cpf != dto.person.cpf:
            raise EntityNotFoundException(entity_name='Person')
        
        person = self.person_gateway.get_by_id(customer.person.id)
        if not person:
            raise EntityNotFoundException(entity_name='Person')
        
        person.cpf = dto.person.cpf
        person.name = dto.person.name
        person.email = dto.person.email
        person.birth_date = dto.person.birth_date

        self.person_gateway.update(person)

        customer.person_id = person.id
        customer.person = person

        customer = self.customer_gateway.update(customer)

        return customer
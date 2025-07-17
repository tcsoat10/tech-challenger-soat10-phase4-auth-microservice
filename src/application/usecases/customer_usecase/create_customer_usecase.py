from src.core.ports.auth.i_auth_provider_gateway import IAuthProviderGateway
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.entities.customer import Customer
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.person import Person


class CreateCustomerUsecase:
    def __init__(self, customer_gateway: ICustomerRepository, person_gateway: IPersonRepository, auth_provider_gateway: IAuthProviderGateway):
        self.customer_gateway = customer_gateway
        self.person_gateway = person_gateway
        self.auth_provider_gateway = auth_provider_gateway

    @classmethod
    def build(
        cls,
        customer_gateway: ICustomerRepository,
        person_gateway: IPersonRepository,
        auth_provider_gateway: IAuthProviderGateway
    ) -> 'CreateCustomerUsecase':
        return cls(customer_gateway, person_gateway, auth_provider_gateway)
    
    def execute(self, dto: CreateCustomerDTO) -> Customer:
        person = self.person_gateway.get_by_cpf(dto.person.cpf)
        if not person:
            if self.person_gateway.exists_by_email(dto.person.email):
                raise EntityDuplicatedException(entity_name='Customer')
            
            person = Person(
                name=dto.person.name,
                cpf=dto.person.cpf,
                email=dto.person.email,
                birth_date=dto.person.birth_date
            )
            person = self.person_gateway.create(person)
        else:
            person.name = dto.person.name
            person.email = dto.person.email
            person.birth_date = dto.person.birth_date
            if person.is_deleted():
                person.reactivate()
            person = self.person_gateway.update(person)
        
        customer = self.customer_gateway.get_by_person_id(person.id)
        if customer:
            if not customer.is_deleted():
                raise EntityDuplicatedException(entity_name='Customer')
            
            customer.reactivate()
            self.customer_gateway.update(customer)
        
        else:
            customer = Customer(person=person)
            customer = self.customer_gateway.create(customer)
            
        self.auth_provider_gateway.sync_user(person=customer.person)
        
        return customer

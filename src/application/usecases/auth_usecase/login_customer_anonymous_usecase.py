
from typing import Any, Dict
import uuid
from src.core.domain.entities.customer import Customer
from src.core.domain.entities.person import Person
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.utils.jwt_util import JWTUtil


class LoginCustomerAnonymousUseCase:
    def __init__(self, customer_gateway: ICustomerRepository, profile_gateway: IProfileRepository):
        self.customer_gateway = customer_gateway
        self.profile_gateway = profile_gateway
        
    @classmethod
    def build(cls, customer_gateway: ICustomerRepository, profile_gateway: IProfileRepository) -> "LoginCustomerAnonymousUseCase":
        return cls(customer_gateway, profile_gateway)

    def execute(self) -> Dict[str, Any]:
        customer_profile = self.profile_gateway.get_by_name("customer")
        if not customer_profile:
            raise EntityNotFoundException(entity_name="Customer profile")
        
        anonymous_person = Person(name=f"Anonymous User - {uuid.uuid4().hex}")
        customer = Customer(person=anonymous_person)
        customer = self.customer_gateway.create(customer)

        token_payload = {
            "person": {
                "id": customer.id,
                "name": customer.person.name,
            },
            "profile": {
                "name": customer_profile.name,
                "permissions": [permission.name for permission in customer_profile.permissions],
            },
        }

        token = JWTUtil.create_token(token_payload)
        return {
            "token_type": "bearer",
            "access_token": token,
        }

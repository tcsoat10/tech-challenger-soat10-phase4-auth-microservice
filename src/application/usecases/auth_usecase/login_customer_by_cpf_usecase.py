
from typing import Any, Dict
from src.core.ports.auth.i_auth_provider_gateway import IAuthProviderGateway
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO
from src.core.domain.entities.customer import Customer
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.invalid_credentials_exception import InvalidCredentialsException
from src.core.utils.jwt_util import JWTUtil
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository


class LoginCustomerByCpfUseCase:
    
    def __init__(self, customer_gateway: ICustomerRepository, profile_gateway: IProfileRepository, auth_provider_gateway: IAuthProviderGateway):
        self.customer_gateway = customer_gateway
        self.profile_gateway = profile_gateway
        self.auth_provider_gateway = auth_provider_gateway
        
    @classmethod
    def build(
        cls,
        customer_gateway: ICustomerRepository,
        profile_gateway: IProfileRepository,
        auth_provider_gateway: IAuthProviderGateway
    ) -> 'LoginCustomerByCpfUseCase':
        return cls(customer_gateway, profile_gateway, auth_provider_gateway)
    
    def execute(self, dto: AuthByCpfDTO) -> Dict[str, Any]:
        # customer_exists = self.auth_provider_gateway.authenticate(dto.cpf)
        # if customer_exists is False:
        #     raise InvalidCredentialsException()

        customer: Customer = self.customer_gateway.get_by_cpf(dto.cpf)
        if not customer:
            raise EntityNotFoundException(entity_name="Customer")
        
        if customer.is_deleted():
            raise InvalidCredentialsException()

        customer_profile = self.profile_gateway.get_by_name("customer")
        if not customer_profile:
            raise EntityNotFoundException(entity_name="Customer profile")

        permissions = [permission.name for permission in customer_profile.permissions]
        if not permissions:
            raise EntityNotFoundException(entity_name="Customer permissions")

        token_payload = {
            "person": {
                "id": str(customer.id),
                "name": customer.person.name,
                "cpf": customer.person.cpf,
                "email": customer.person.email,
            },
            "profile": {
                "name": customer_profile.name,
                "permissions": permissions,
            },
        }

        token = JWTUtil.create_token(token_payload)
        return {
            "token_type": "bearer",
            "access_token": token,
        }

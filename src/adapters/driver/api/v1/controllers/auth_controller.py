
from src.core.ports.auth.i_auth_provider_gateway import IAuthProviderGateway
from src.application.usecases.auth_usecase.login_employee_usecase import LoginEmployeeUseCase
from src.application.usecases.auth_usecase.login_customer_anonymous_usecase import LoginCustomerAnonymousUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.auth_usecase.login_customer_by_cpf_usecase import LoginCustomerByCpfUseCase
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO, TokenDTO
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository

class AuthController:
    def __init__(
        self,
        profile_gateway: IProfileRepository,
        employee_gateway: IEmployeeRepository,
        customer_gateway: ICustomerRepository,
        auth_provider_gateway: IAuthProviderGateway,
    ):
        self.profile_gateway: IProfileRepository = profile_gateway
        self.employee_gateway: IEmployeeRepository = employee_gateway
        self.customer_gateway: ICustomerRepository = customer_gateway
        self.auth_provider_gateway: IAuthProviderGateway = auth_provider_gateway
        
    def login_customer_by_cpf(self, dto: AuthByCpfDTO) -> TokenDTO:
        login_customer_by_cpf_use_case = LoginCustomerByCpfUseCase.build(self.customer_gateway, self.profile_gateway, self.auth_provider_gateway)
        token = login_customer_by_cpf_use_case.execute(dto)
        return DTOPresenter.transform_from_dict(token, TokenDTO)
    
    def login_customer_anonymous(self) -> TokenDTO:
        login_customer_anonymous_use_case = LoginCustomerAnonymousUseCase.build(self.customer_gateway, self.profile_gateway)
        token = login_customer_anonymous_use_case.execute()
        return DTOPresenter.transform_from_dict(token, TokenDTO)
    
    def login_employee(self, dto: LoginDTO) -> TokenDTO:
        login_employee_use_case = LoginEmployeeUseCase.build(self.employee_gateway, self.profile_gateway)
        token = login_employee_use_case.execute(dto)
        return DTOPresenter.transform_from_dict(token, TokenDTO)

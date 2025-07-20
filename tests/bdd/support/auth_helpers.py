from src.application.usecases.auth_usecase.login_customer_anonymous_usecase import LoginCustomerAnonymousUseCase
from src.application.usecases.auth_usecase.login_customer_by_cpf_usecase import LoginCustomerByCpfUseCase
from src.application.usecases.auth_usecase.login_employee_usecase import LoginEmployeeUseCase
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO
from src.core.domain.entities.customer import Customer
from src.core.domain.entities.employee import Employee
from src.core.domain.entities.permission import Permission
from src.core.domain.entities.profile import Profile
from src.core.domain.entities.profile_permission import ProfilePermission
from src.core.domain.entities.role import Role
from src.core.utils.jwt_util import JWTUtil
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.adapters.driven.repositories.profile_permission_repository import ProfilePermissionRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.adapters.driven.auth_providers.aws_cognito_gateway import AWSCognitoGateway

class AuthTestHelper:
    """Helper para operações de autenticação em testes BDD"""
    
    def __init__(self, db_session):
        self.db_session = db_session
        self.customer_repo = CustomerRepository(db_session)
        self.person_repo = PersonRepository(db_session)
        self.profile_repo = ProfileRepository(db_session)
        self.permission_repo = PermissionRepository(db_session)
        self.profile_permission_repo = ProfilePermissionRepository(db_session)
        self.employee_repo = EmployeeRepository(db_session)
        self.user_repo = UserRepository(db_session)
        self.role_repo = RoleRepository(db_session)
        self.auth_provider = AWSCognitoGateway()

    def create_profile(self, profile: Profile):
        return self.profile_repo.create(profile)

    def get_profile_by_name(self, name: str):
        return self.profile_repo.get_by_name(name)

    def reload_profile_with_permissions(self, profile: Profile):
        return self.profile_repo.get_by_name(profile.name)

    def create_permission(self, permission: Permission):
        return self.permission_repo.create(permission)

    def get_permission_by_name(self, name: str):
        return self.permission_repo.get_by_name(name)

    def create_profile_permission(self, profile_permission: ProfilePermission):
        return self.profile_permission_repo.create(profile_permission)

    def associate_profile_with_permissions(self, profile: Profile, permissions: list[Permission]):
        profile_permissions = []
        for permission in permissions:
            profile_permission = ProfilePermission(profile=profile, permission=permission)
            created_pp = self.profile_permission_repo.create(profile_permission)
            profile_permissions.append(created_pp)

        profile.permissions = permissions
        return profile_permissions

    def create_customer(self, customer: Customer):
        created_person = self.person_repo.create(customer.person)
        customer.person = created_person
        return self.customer_repo.create(customer)

    def create_role(self, role: Role):
        return self.role_repo.create(role)

    def create_employee(self, employee: Employee):
        created_person = self.person_repo.create(employee.person)
        created_user = self.user_repo.create(employee.user)
        employee.person = created_person
        employee.user = created_user
        return self.employee_repo.create(employee)

    def login_by_cpf(self, dto: AuthByCpfDTO):
        use_case = LoginCustomerByCpfUseCase(
            self.customer_repo, 
            self.profile_repo, 
            self.auth_provider
        )
        return use_case.execute(dto)

    def login_employee(self, dto: LoginDTO):
        use_case = LoginEmployeeUseCase(self.employee_repo, self.profile_repo)
        return use_case.execute(dto)

    def login_anonymous(self):
        use_case = LoginCustomerAnonymousUseCase(self.customer_repo, self.profile_repo)
        return use_case.execute()

    def decode_token(self, token: str):
        return JWTUtil.decode_token(token)

from dependency_injector import containers, providers

from config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.auth_providers.aws_cognito_gateway import AWSCognitoGateway
from src.adapters.driver.api.v1.controllers.auth_controller import AuthController
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.adapters.driver.api.v1.controllers.permission_controller import PermissionController
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.adapters.driver.api.v1.controllers.profile_controller import ProfileController
from src.adapters.driven.repositories.profile_permission_repository import ProfilePermissionRepository
from src.adapters.driver.api.v1.controllers.profile_permission_controller import ProfilePermissionController
from src.adapters.driven.repositories.user_repository import UserRepository
from src.adapters.driver.api.v1.controllers.user_controller import UserController
from src.adapters.driven.repositories.user_profile_repository import UserProfileRepository
from src.adapters.driver.api.v1.controllers.user_profile_controller import UserProfileController
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.adapters.driver.api.v1.controllers.person_controller import PersonController
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driver.api.v1.controllers.customer_controller import CustomerController
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.adapters.driver.api.v1.controllers.role_controller import RoleController
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driver.api.v1.controllers.employee_controller import EmployeeController


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.adapters.driver.api.v1.controllers.permission_controller",
        "src.adapters.driver.api.v1.routes.permission_routes",
        "src.adapters.driver.api.v1.controllers.profile_controller",
        "src.adapters.driver.api.v1.routes.profile_routes",
        "src.adapters.driver.api.v1.controllers.profile_permission_controller",
        "src.adapters.driver.api.v1.routes.profile_permission_routes",
        "src.adapters.driver.api.v1.controllers.user_controller",
        "src.adapters.driver.api.v1.routes.user_routes",
        "src.adapters.driver.api.v1.controllers.user_profile_controller",
        "src.adapters.driver.api.v1.routes.user_profile_routes",
        "src.adapters.driver.api.v1.controllers.person_controller",
        "src.adapters.driver.api.v1.routes.person_routes",
        "src.adapters.driver.api.v1.controllers.customer_controller",
        "src.adapters.driver.api.v1.routes.customer_routes",
        "src.adapters.driver.api.v1.controllers.role_controller",
        "src.adapters.driver.api.v1.routes.role_routes",
        "src.adapters.driver.api.v1.controllers.employee_controller",
        "src.adapters.driver.api.v1.routes.employee_routes",
        "src.adapters.driver.api.v1.controllers.auth_controller",
        "src.adapters.driver.api.v1.routes.auth_routes",
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)

    permission_gateway = providers.Factory(PermissionRepository, db_session=db_session)
    permission_controller = providers.Factory(PermissionController, permission_gateway=permission_gateway)

    profile_gateway = providers.Factory(ProfileRepository, db_session=db_session)
    profile_controller = providers.Factory(ProfileController, profile_gateway=profile_gateway)

    profile_permission_gateway = providers.Factory(ProfilePermissionRepository, db_session=db_session)
    profile_permission_controller = providers.Factory(
        ProfilePermissionController,
        profile_permission_gateway=profile_permission_gateway,
        permission_gateway=permission_gateway,
        profile_gateway=profile_gateway
    )

    user_gateway = providers.Factory(UserRepository, db_session=db_session)
    user_controller = providers.Factory(UserController, user_gateway=user_gateway)

    user_profile_gateway = providers.Factory(UserProfileRepository, db_session=db_session)
    user_profile_controller = providers.Factory(
        UserProfileController,
        user_profile_gateway=user_profile_gateway,
        profile_gateway=profile_gateway,
        user_gateway=user_gateway
    )

    person_gateway = providers.Factory(PersonRepository, db_session=db_session)
    person_controller = providers.Factory(PersonController, person_gateway=person_gateway)

    auth_provider_gateway = providers.Factory(AWSCognitoGateway)

    customer_gateway = providers.Factory(CustomerRepository, db_session=db_session)
    customer_controller = providers.Factory(
        CustomerController,
        customer_gateway=customer_gateway,
        person_gateway=person_gateway,
        auth_provider_gateway=auth_provider_gateway,
    )

    role_gateway = providers.Factory(RoleRepository, db_session=db_session)
    role_controller = providers.Factory(RoleController, role_gateway=role_gateway)

    employee_gateway = providers.Factory(EmployeeRepository, db_session=db_session)
    employee_controller = providers.Factory(
        EmployeeController,
        employee_gateway=employee_gateway,
        person_gateway=person_gateway,
        role_gateway=role_gateway,
        user_gateway=user_gateway
    )
    
    auth_controller = providers.Factory(
        AuthController,
        profile_gateway=profile_gateway,
        employee_gateway=employee_gateway,
        customer_gateway=customer_gateway,
        auth_provider_gateway=auth_provider_gateway            
    )
    

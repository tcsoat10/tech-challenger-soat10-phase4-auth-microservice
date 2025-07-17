import os
from faker import Faker
import pytest
from typing import Dict, Generator, List, Optional
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from src.core.containers import Container
from src.app import app
from config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.core.utils.jwt_util import JWTUtil
from tests.factories.employee_factory import EmployeeFactory
from tests.factories.permission_factory import PermissionFactory
from tests.factories.profile_factory import ProfileFactory
from tests.factories.profile_permission_factory import ProfilePermissionFactory
from tests.factories.role_factory import RoleFactory
from tests.factories.user_factory import UserFactory
from tests.factories.user_profile_factory import UserProfileFactory
from tests.factories.person_factory import PersonFactory
from tests.factories.customer_factory import CustomerFactory


@pytest.fixture(scope="function")
def test_engine(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("data") / "test.sqlite"
    db_url = f"sqlite:///{db_file}"
    engine = create_engine(db_url, echo=False)

    envs_to_override = {
        'ENVIRONMENT': 'testing',
    }

    for key, value in envs_to_override.items():
        os.environ[key] = value

    # Configura e roda Alembic
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    try:
        command.upgrade(alembic_cfg, "head")
        print("Migrações Alembic aplicadas no SQLite.")
    except Exception as e:
        pytest.fail(f"Erro ao aplicar migrações Alembic no SQLite: {e}")

    yield engine
    engine.dispose() # Fecha conexões, arquivo é removido pelo pytest

@pytest.fixture(scope="function")
def db_session(test_engine):
    SessionLocal = sessionmaker(bind=test_engine)
    session = SessionLocal()

    # Override de dependência do FastAPI e Container
    def override_get_db():
        try:
            yield session
        finally:
            pass # Sessão é fechada no finally principal

    app.dependency_overrides[get_db] = override_get_db
    container = Container()
    container.db_session.override(session)
    app.container = container

    try:
        yield session
    finally:
        session.close()
        app.dependency_overrides.pop(get_db, None)
        # Limpeza do IdentityMap se necessário
        identity_map = IdentityMap.get_instance()
        identity_map.clear()


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """
    Cria um cliente de teste para a aplicação.
    Permissões devem ser informadas manualmente para cada requisição, caso contrário, serão vazias.
    """
    def create_mock_token(permissions: List[str], profile_name: Optional[str], person: Optional[dict]) -> str:
        fake = Faker("pt_BR")
        mock_payload = {
            "profile": {
                "name": profile_name,
                "permissions": permissions,
            },
            "person": person or {
                "id": "1",
                "name": "Test User",
                "cpf": fake.ssn(),
                "email": fake.email()
            }
        }
        return JWTUtil.create_token(mock_payload)

    def override_headers(headers: Dict[str, str] = None, permissions: List[str] = None, profile_name: Optional[str] = "administrator", person: Optional[dict] = None) -> Dict[str, str]:
        if headers is None:
            headers = {}
        token = create_mock_token(permissions or [], profile_name, person)
        headers.update({"Authorization": f"Bearer {token}"})
        return headers

    with TestClient(app) as test_client:
        def with_permissions(method, url, person: Optional[dict] = None, permissions=None, profile_name: Optional[str] = "administrator", **kwargs):
            headers = kwargs.pop("headers", {})
            kwargs["headers"] = override_headers(headers, permissions=permissions, profile_name=profile_name, person=person)
            return method(url, **kwargs)

        test_client._original_get = test_client.get
        test_client._original_post = test_client.post
        test_client._original_put = test_client.put
        test_client._original_delete = test_client.delete

        test_client.get = lambda url, permissions=None, **kwargs: with_permissions(
            test_client._original_get, url, permissions=permissions, **kwargs
        )
        test_client.post = lambda url, permissions=None, **kwargs: with_permissions(
            test_client._original_post, url, permissions=permissions, **kwargs
        )
        test_client.put = lambda url, permissions=None, **kwargs: with_permissions(
            test_client._original_put, url, permissions=permissions, **kwargs
        )
        test_client.delete = lambda url, permissions=None, **kwargs: with_permissions(
            test_client._original_delete, url, permissions=permissions, **kwargs
        )

        yield test_client

@pytest.fixture(scope="function", autouse=True)
def setup_factories(db_session):
    """
    Configura as factories para usar a sessão do banco de dados de teste.
    """
    factories = [
        PermissionFactory,
        ProfileFactory,
        ProfilePermissionFactory,
        RoleFactory,
        UserFactory,
        UserProfileFactory,
        PersonFactory,
        CustomerFactory,
        EmployeeFactory,
    ]
    
    identity_map = IdentityMap.get_instance()

    def after_postgeneration(obj):
        """
        Post-generation hook to add the entity to the identity map.
        
        Args:
            obj: The generated object.
        """
        if hasattr(obj, 'to_entity'):
            entity = obj.to_entity()
            identity_map.add(entity)
        return obj

    for factory in factories:
        factory._meta.sqlalchemy_session = db_session
        factory.reset_sequence()
        factory._meta.after_postgeneration = after_postgeneration

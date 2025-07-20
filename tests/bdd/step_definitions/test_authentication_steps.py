import pytest
from pytest_bdd import scenarios, given
from tests.bdd.support.auth_helpers import AuthTestHelper

scenarios('../features/authentication.feature')

@pytest.fixture
def auth_helper(db_session):
    return AuthTestHelper(db_session)

@given('que o sistema está funcionando')
def system_is_running(db_session):
    assert db_session is not None

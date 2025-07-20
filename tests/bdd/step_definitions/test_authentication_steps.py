import pytest
from pytest_bdd import scenarios
from tests.bdd.support.auth_helpers import AuthTestHelper

scenarios('../features/authentication.feature')

@pytest.fixture
def auth_helper(db_session):
    return AuthTestHelper(db_session)

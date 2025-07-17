import pytest

from src.adapters.driven.repositories.models.profile_permission_model import ProfilePermissionModel
from src.adapters.driven.repositories.profile_permission_repository import ProfilePermissionRepository
from src.core.domain.entities.profile_permission import ProfilePermission
from tests.factories.permission_factory import PermissionFactory
from tests.factories.profile_factory import ProfileFactory
from tests.factories.profile_permission_factory import ProfilePermissionFactory

class TestProfilePermissionRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = ProfilePermissionRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(ProfilePermissionModel).delete()
        self.db_session.commit()

    def test_create_profile_permission_success(self):
        profile = ProfileFactory()
        permission = PermissionFactory()
        profile_permission = ProfilePermission(profile=profile.to_entity(), permission=permission.to_entity())

        created_profile_permission = self.repository.create(profile_permission)

        assert created_profile_permission.id is not None
        assert created_profile_permission.profile.id == profile.id
        assert created_profile_permission.permission.id == permission.id

    def test_get_profile_permission_by_profile_permission_id_success(self):
        profile_permission = ProfilePermissionFactory()

        profile_permission_response = self.repository.get_by_id(profile_permission_id=profile_permission.id)

        assert profile_permission_response is not None
        assert profile_permission_response.id == profile_permission.id
        assert profile_permission_response.permission.id == profile_permission.permission_id
        assert profile_permission_response.profile.id == profile_permission.profile_id

    def test_get_profile_permission_by_profile_permission_id_returns_none_for_unregistered_id(self):
        profile_permission = self.repository.get_by_id(profile_permission_id=1)
        assert profile_permission is None
    
    def test_get_profile_permission_by_profile_id_success(self, db_session):
        profile_permission = ProfilePermissionFactory()

        profile_permission_response = self.repository.get_by_profile_id(profile_id=profile_permission.profile_id)

        assert profile_permission_response.id is not None
        assert profile_permission_response.profile.id == profile_permission.profile_id
        assert profile_permission_response.permission.id == profile_permission.permission_id

    def test_get_profile_permission_by_permission_id_success(self, db_session):
        profile_permission = ProfilePermissionFactory()

        profile_permission_response = self.repository.get_by_permission_id(permission_id=profile_permission.permission_id)

        assert profile_permission_response.id is not None
        assert profile_permission_response.profile.id == profile_permission.profile_id
        assert profile_permission_response.permission.id == profile_permission.permission_id
    
    def test_get_profile_permission_by_profile_id_returns_none_for_unregistered_id(self):
        profile_permission = self.repository.get_by_profile_id(profile_id=1)

        assert profile_permission is None

    def test_get_profile_permission_by_permission_id_returns_none_for_unregistered_id(self):
        profile_permission = self.repository.get_by_permission_id(permission_id=1)

        assert profile_permission is None
    
    def test_get_all_profile_permissions_return_success(self):
        profile_permission1 = ProfilePermissionFactory()
        profile_permission2 = ProfilePermissionFactory()

        profile_permissions = self.repository.get_all()

        assert len(profile_permissions) == 2

        assert profile_permissions[0].id == profile_permission1.id
        assert profile_permissions[0].profile.id == profile_permission1.profile_id
        assert profile_permissions[0].permission.id == profile_permission1.permission_id
        
        assert profile_permissions[1].id == profile_permission2.id
        assert profile_permissions[1].profile.id == profile_permission2.profile_id
        assert profile_permissions[1].permission.id == profile_permission2.permission_id
        
        

    def test_get_all_profile_permissions_with_empty_db(self):
        profile_permissions = self.repository.get_all()

        assert len(profile_permissions) == 0
        assert profile_permissions == []

    def test_update_profile_permission(self):
        profile_permission = ProfilePermissionFactory()
        permission = PermissionFactory()
        profile = ProfileFactory()

        profile_permission.permission_id = permission.id
        profile_permission.profile_id = profile.id

        data = self.repository.update(profile_permission)

        assert data.id == profile_permission.id
        assert data.profile.id == profile.id
        assert data.permission.id == permission.id

    def test_delete_profile_permission(self):
        profile_permission1 = ProfilePermissionFactory()
        profile_permission2 = ProfilePermissionFactory()

        self.repository.delete(profile_permission1)
        data = self.repository.get_all()

        assert len(data) == 1
        assert data[0].id == profile_permission2.id
        assert data[0].profile.id == profile_permission2.profile_id
        assert data[0].permission.id == profile_permission2.permission_id




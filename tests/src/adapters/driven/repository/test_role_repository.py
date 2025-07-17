import pytest
from sqlalchemy.exc import IntegrityError

from src.adapters.driven.repositories.models.role_model import RoleModel
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.core.domain.entities.role import Role
from tests.factories.role_factory import RoleFactory




class TestRoleRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = RoleRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(RoleModel).delete()
        self.db_session.commit()

    def test_create_role_success(self):
        admin_role = Role(name='Admin', description='Admin role')
        created_admin_role = self.repository.create(admin_role)

        assert created_admin_role.id is not None
        assert created_admin_role.name == admin_role.name
        assert created_admin_role.description == admin_role.description

    def test_create_duplicate_role_return_error(self):
        admin_role = Role(name='Admin', description='Admin role')
        self.repository.create(admin_role)

        duplicate_role = Role(name='Admin', description='Admin role - new')

        with pytest.raises(IntegrityError):
            self.repository.create(duplicate_role)
    
    def test_get_role_by_name_success(self):
        new_role = RoleFactory()

        role = self.repository.get_by_name(new_role.name)

        assert role is not None
        assert role.id == new_role.id
        assert role.name == new_role.name
        assert role.description == new_role.description
    
    def test_get_role_by_name_with_unregistered_name(self):
        RoleFactory(name='registered name')

        role = self.repository.get_by_name('not a name')

        assert role is None

    def test_get_role_by_id_and_return_success(self):
        new_role = RoleFactory()

        role = self.repository.get_by_id(new_role.id)

        assert role is not None
        assert role.id == new_role.id
        assert role.name == new_role.name
        assert role.description == new_role.description

    def test_get_role_by_id_with_unregistered_id(self):
        new_role = RoleFactory()

        role = self.repository.get_by_id(new_role.id + 1)

        assert role is None

    def test_get_all_roles(self):
        role1 = RoleFactory()
        role2 = RoleFactory()

        roles = self.repository.get_all()

        assert len(roles) == 2
        assert roles[0].name == role1.name
        assert roles[1].name == role2.name

    def test_get_all_roles_with_empty_db(self):
        roles = self.repository.get_all()

        assert len(roles) == 0
        assert roles == []
    
    def test_update_role(self):
        role = RoleFactory()

        role.name = 'New name'
        role.description = 'New description'

        updated_role = self.repository.update(role)

        assert updated_role.name == 'New name'
        assert updated_role.description == 'New description'
    
    def test_delete_role(self):
        role = RoleFactory()

        assert len(self.repository.get_all()) == 1
        
        self.repository.delete(role)

        assert len(self.repository.get_all()) == 0

    def test_delete_role_with_inexistent_id(self):
        RoleFactory(name='registered role', description='registered role')
        
        unregistered_role = Role(name='Unregistered role', description='Unregistered role')
        
        self.repository.delete(unregistered_role)

        roles = self.repository.get_all()
        assert len(roles) == 1
        assert roles[0].name == 'registered role'
        assert roles[0].description == 'registered role'

import pytest
from sqlalchemy.exc import IntegrityError

from src.adapters.driven.repositories.models.user_model import UserModel
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.domain.entities.user import User
from tests.factories.user_factory import UserFactory


class TestUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = UserRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(UserModel).delete()
        self.db_session.commit()

    def test_create_user_success(self):
        new_user = User(name='Test User', password='test_pass')
        created_user = self.repository.create(new_user)

        assert created_user.id is not None
        assert created_user.name == new_user.name
        assert created_user.verify_password('test_pass') is True
    
    def test_verify_wrong_password_return_error(self):
        user_model = UserFactory(password='test_pass')
        user = user_model.to_entity()
        assert user.verify_password('wrong_pass') is False

    def test_create_duplicate_user_return_error(self):
        user1 = UserFactory(name='user1')

        user2 = User(name='user1', password='test_pass')
        with pytest.raises(IntegrityError):
            self.repository.create(user2)

    def test_get_user_by_name_return_success(self):
        new_user = UserFactory(name='user')

        user = self.repository.get_by_name(new_user.name)

        assert user is not None
        assert new_user.id == user.id
        assert user.name == new_user.name

    def test_get_user_by_name_with_unregistered_name(self):
        UserFactory()
        
        user = self.repository.get_by_name('not a name')

        assert user is None

    def test_get_user_by_id_return_success(self):
        new_user = UserFactory()

        user = self.repository.get_by_id(new_user.id)

        assert user is not None
        assert user.id == new_user.id
        assert user.name == new_user.name

    def test_get_user_by_id_with_unregistered_id(self):
        new_user = UserFactory()

        user = self.repository.get_by_id(new_user.id + 1)

        assert user is None
    
    def test_get_all_users_return_success(self):
        user1 = UserFactory()
        user2 = UserFactory()

        users = self.repository.get_all()

        assert len(users) == 2
        assert users[0].name == user1.name
        assert users[1].name == user2.name

    def test_get_all_users_with_empty_db(self):
        users = self.repository.get_all()

        assert len(users) == 0
        assert users == []

    def test_update_user(self):
        user_model = UserFactory(name='user1', password='test_pass')

        user = user_model.to_entity()
        user.name = 'user2'
        user.password = 'new_pass'

        updated_user = self.repository.update(user)

        assert updated_user.name == user.name
        assert updated_user.verify_password('test_pass') is False
        assert updated_user.verify_password('new_pass') is True

    def test_delete_user(self):
        user = UserFactory()

        self.repository.delete(user.id)

        assert len(self.repository.get_all()) == 0

    def test_delete_user_with_unregistered_id(self):
        user = UserFactory()

        self.repository.delete(user.id + 1)

        assert len(self.repository.get_all()) == 1

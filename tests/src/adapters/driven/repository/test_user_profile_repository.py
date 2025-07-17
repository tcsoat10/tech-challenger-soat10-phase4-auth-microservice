
import pytest

from sqlalchemy.orm import Session
from src.adapters.driven.repositories.models.user_profile_model import UserProfileModel
from src.core.domain.entities.user_profile import UserProfile
from src.adapters.driven.repositories.user_profile_repository import UserProfileRepository
from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from tests.factories.profile_factory import ProfileFactory
from tests.factories.user_factory import UserFactory
from tests.factories.user_profile_factory import UserProfileFactory


class TestUserProfileRepository:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository: IUserProfileRepository = UserProfileRepository(db_session)
        self.db_session: Session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(UserProfileModel).delete()
        self.db_session.commit()
    
    def test_create_user_profile_success(self):
        user_model = UserFactory(id=1)
        profile_model = ProfileFactory(id=1)

        user_profile = UserProfile(user=user_model.to_entity(), profile=profile_model.to_entity())
        created_user_profile = self.repository.create(user_profile)

        assert created_user_profile.id is not None
        assert created_user_profile.user.id == user_profile.user.id
        assert created_user_profile.profile.id == user_profile.profile.id

    def test_get_user_profile_by_id_success(self):
        new_user_profile = UserProfileFactory()
        user_profile = self.repository.get_by_id(new_user_profile.id)

        assert user_profile is not None
        assert user_profile.id == new_user_profile.id
        assert user_profile.user.id == new_user_profile.user_id
        assert user_profile.profile.id == new_user_profile.profile_id
    
    def test_get_user_profile_by_id_with_unregistered_id(self):
        UserProfileFactory(id=1)

        user_profile = self.repository.get_by_id(999)

        assert user_profile is None

    def test_get_user_profile_by_user_id_and_profile_id_success(self):
        new_user_profile = UserProfileFactory()
        user_profile = self.repository.get_by_user_id_and_profile_id(new_user_profile.user_id, new_user_profile.profile_id)

        assert user_profile is not None
        assert user_profile.id == new_user_profile.id
        assert user_profile.user.id == new_user_profile.user_id
        assert user_profile.profile.id == new_user_profile.profile_id

    def test_get_user_profile_by_user_id_and_profile_id_with_unregistered_ids(self):
        UserProfileFactory()

        user_profile = self.repository.get_by_user_id_and_profile_id(999, 999)

        assert user_profile is None
    
    def test_get_all_user_profiles_success(self):
        UserProfileFactory.create_batch(3)

        all_user_profiles = self.repository.get_all()

        assert len(all_user_profiles) == 3

    def test_get_all_user_profiles_with_deleted(self):
        user_profiles = UserProfileFactory.create_batch(3)
        self.db_session.add_all(user_profiles)
        self.db_session.commit()

        all_user_profiles = self.repository.get_all(include_deleted=True)

        assert len(all_user_profiles) == 3
    
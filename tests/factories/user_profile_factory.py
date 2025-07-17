
import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from src.adapters.driven.repositories.models.user_model import UserModel
from src.adapters.driven.repositories.models.user_profile_model import UserProfileModel
from tests.factories.profile_factory import ProfileFactory
from tests.factories.user_factory import UserFactory

fake = Faker()

class UserProfileFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserProfileModel
        sqlalchemy_session_persistence = 'commit'


    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute('user.id')
    profile = factory.SubFactory(ProfileFactory)
    profile_id = factory.SelfAttribute('profile.id')
    
    class Params:
        user_model = UserModel

import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory

from src.adapters.driven.repositories.models.profile_permission_model import ProfilePermissionModel
from tests.factories.profile_factory import ProfileFactory
from tests.factories.permission_factory import PermissionFactory


fake = Faker()

class ProfilePermissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ProfilePermissionModel
        sqlalchemy_session_persistence = 'commit'
    

    profile = factory.SubFactory(ProfileFactory)
    profile_id = factory.SelfAttribute('profile.id')
    permission = factory.SubFactory(PermissionFactory)
    permission_id = factory.SelfAttribute('permission.id')
    

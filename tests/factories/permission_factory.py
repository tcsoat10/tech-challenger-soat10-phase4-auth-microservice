import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory

from src.adapters.driven.repositories.models.permission_model import PermissionModel

fake = Faker()

class PermissionFactory(SQLAlchemyModelFactory):

    class Meta:
        model = PermissionModel
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))

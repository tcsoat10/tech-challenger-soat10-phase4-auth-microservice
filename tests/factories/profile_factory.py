import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory

from src.adapters.driven.repositories.models.profile_model import ProfileModel

fake = Faker()

class ProfileFactory(SQLAlchemyModelFactory):

    class Meta:
        model = ProfileModel
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))

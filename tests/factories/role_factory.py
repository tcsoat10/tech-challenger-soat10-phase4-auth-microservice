from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.adapters.driven.repositories.models.role_model import RoleModel


fake = Faker()


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RoleModel
        sqlalchemy_session_persistence = 'commit'


    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=3))
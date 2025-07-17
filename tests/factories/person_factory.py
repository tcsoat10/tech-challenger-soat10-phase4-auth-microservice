import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.adapters.driven.repositories.models.person_model import PersonModel

fake = Faker("pt_BR")

class PersonFactory(SQLAlchemyModelFactory):
    
    class Meta:
        model = PersonModel
        sqlalchemy_session_persistence = "commit"

    cpf = factory.LazyAttribute(lambda _: fake.ssn())
    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.email(safe=True, domain='example.com'))
    birth_date = factory.LazyAttribute(lambda _: fake.date_of_birth(minimum_age=5, maximum_age=100))

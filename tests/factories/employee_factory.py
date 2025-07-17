from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.adapters.driven.repositories.models.employee_model import EmployeeModel
from tests.factories.person_factory import PersonFactory
from tests.factories.role_factory import RoleFactory
from tests.factories.user_factory import UserFactory


fake = Faker()


class EmployeeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = EmployeeModel
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 1)
    admission_date = factory.LazyAttribute(lambda _: fake.past_date())
    termination_date = factory.LazyAttribute(lambda _: fake.future_date())
    person = factory.SubFactory(PersonFactory)
    person_id = factory.SelfAttribute('person.id')
    role = factory.SubFactory(RoleFactory)
    role_id = factory.SelfAttribute('role.id')
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute('user.id')
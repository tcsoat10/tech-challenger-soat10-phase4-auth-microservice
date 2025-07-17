import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from src.core.domain.entities.user import User
from src.adapters.driven.repositories.models.user_model import UserModel

fake = Faker()
class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: fake.name())
    password_hash = factory.LazyAttribute(lambda _: User.hash_password(fake.password()))

    class Params:
        user_entity = User
        password = fake.password()

    @factory.post_generation
    def user_entity(self, create, extracted, **kwargs):
        if not create:
            return

        entity = self.user_entity(id=self.id, name=self.name, password_hash=self.password_hash)

        if extracted:
            for user in extracted:
                entity.user_id = user.user_id

        return entity

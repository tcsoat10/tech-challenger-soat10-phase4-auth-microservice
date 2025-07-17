
from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError

from src.adapters.driven.repositories.models.person_model import PersonModel
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.core.domain.entities.person import Person
from tests.factories.person_factory import PersonFactory


class TestPersonRepository:
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = PersonRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(PersonModel).delete()
        self.db_session.commit()

    def test_create_person_success(self):
        birth = datetime.strptime("01/01/1999", "%d/%m/%Y")
        person = Person(cpf= "12345678901", name="JOÃO", email="joao@gmail.com", birth_date=birth)
        created_person = self.repository.create(person)

        assert created_person.id is not None
        assert created_person.cpf == "12345678901"
        assert created_person.name == "JOÃO"
        assert created_person.email == "joao@gmail.com"
        assert created_person.birth_date == datetime.date(birth)


        '''db_person = self.db_session.query(Person).filter_by(name="JOÃO").first()
        assert db_person is not None
        assert db_person.cpf == "12345678901"
        assert db_person.name == "JOÃO"
        assert db_person.email == "joao@gmail.com"
        assert db_person.birth_date == birth'''

    def test_exists_by_cpf_success(self):
        person = PersonFactory()

        assert self.repository.exists_by_cpf(person.cpf) is True

    def test_exists_by_cpf_failure(self):
        assert self.repository.exists_by_cpf("0000000000") is False

    def test_try_create_person_duplicated_with_repository_and_raise_error(self):
        person1 = PersonFactory()

        person2 = Person(cpf=person1.cpf, name=person1.name, email="joao@gmail.com")
        with pytest.raises(IntegrityError):
            self.repository.create(person2)

    def test_get_by_cpf_success(self):
        new_person = PersonFactory()

        person = self.repository.get_by_cpf(new_person.cpf)

        assert person is not None
        assert person.id == new_person.id
        assert person.cpf == new_person.cpf
        assert person.name == new_person.name
        assert person.email == new_person.email

    @pytest.mark.skip(reason="Not implemented yet")
    def test_get_person_by_name_with_unregistered_name(self):
        PersonFactory()

        person = self.repository.get_by_name('not a name')

        assert person is None

    def test_get_by_id_success(self):
        new_person = PersonFactory()

        person = self.repository.get_by_id(new_person.id)

        assert person is not None
        assert person.id == new_person.id
        assert person.name == new_person.name
        assert person.email == new_person.email

    def test_get_all_success(self):
        person1 = PersonFactory()
        person2 = PersonFactory()

        persons = self.repository.get_all()

        assert len(persons) == 2
        assert persons[0].id == person1.id
        assert persons[0].name == person1.name
        assert persons[0].email == person1.email
        assert persons[1].id == person2.id
        assert persons[1].name == person2.name
        assert persons[1].email == person2.email
    
    def test_get_all_persons_empty_db(self):
        persons = self.repository.get_all()

        assert len(persons) == 0
        assert persons == []
    
    def test_update_person_success(self):
        person = PersonFactory()

        person.name = "PAULO"
        person.email = "paulo@outlook.com"
        updated_person = self.repository.update(person)

        assert updated_person.id is not None
        assert updated_person.id == person.id
        assert updated_person.name == "PAULO"
        assert updated_person.email == "paulo@outlook.com"

    def test_delete_person_success(self): 
        person = PersonFactory()

        self.repository.delete(person.id)

        persons = self.repository.get_all()

        assert len(persons) == 0
        assert persons == []

    def test_delete_person_unregistered_id(self): 
        person = PersonFactory()

        self.repository.delete(person.id + 1)

        persons = self.repository.get_all()

        assert len(persons) == 1
        assert persons[0].id == person.id
        assert persons[0].name == person.name
        assert persons[0].email == person.email


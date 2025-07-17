from typing import List
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.person_model import PersonModel
from src.core.domain.entities.person import Person
from src.core.ports.person.i_person_repository import IPersonRepository


class PersonRepository(IPersonRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, person: Person) -> Person:
        if person.id is not None:
            existing = self.identity_map.get(Person, person.id)
            if existing:
                self.identity_map.remove(existing)
        
        person_model = PersonModel.from_entity(person)
        self.db_session.add(person_model)
        self.db_session.commit()
        self.db_session.refresh(person_model)
        return person_model.to_entity()

    def exists_by_cpf(self, cpf: str) -> bool:
        return self.db_session.query(exists().where(PersonModel.cpf == cpf)).scalar()
    
    def exists_by_email(self, email: str) -> bool:
        return self.db_session.query(exists().where(PersonModel.email == email)).scalar()

    def get_by_cpf(self, cpf: str) -> Person:
        person_model = self.db_session.query(PersonModel).filter(PersonModel.cpf == cpf).first()
        if person_model is None:
            return None
        return person_model.to_entity()

    def get_by_id(self, person_id: int) -> Person:
        person_model = self.db_session.query(PersonModel).filter(PersonModel.id == person_id).first()
        if person_model is None:
            return None
        return person_model.to_entity()

    def get_all(self, include_deleted: bool = False) -> List[Person]:
        query = self.db_session.query(PersonModel)
        if not include_deleted:
            query = query.filter(PersonModel.inactivated_at.is_(None))
        persons_models = query.all()
        return [person_model.to_entity() for person_model in persons_models]

    def update(self, person: Person) -> Person:
        existing = self.identity_map.get(Person, person.id)
        if existing:
            self.identity_map.remove(existing)
        person_model = PersonModel.from_entity(person)
        self.db_session.merge(person_model)
        self.db_session.commit()
        return person_model.to_entity()

    def delete(self, person_id: int) -> None:
        person_model = self.db_session.query(PersonModel).filter(PersonModel.id == person_id).first()
        if person_model is not None:
            self.db_session.delete(person_model)
            self.db_session.commit()
            self.identity_map.remove(person_model.to_entity())

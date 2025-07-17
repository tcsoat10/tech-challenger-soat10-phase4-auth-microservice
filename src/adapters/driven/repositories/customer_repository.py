from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.customer_model import CustomerModel
from src.adapters.driven.repositories.models.person_model import PersonModel
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.domain.entities.customer import Customer

from sqlalchemy.orm import Session
from typing import List


class CustomerRepository(ICustomerRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, customer: Customer) -> Customer:
        if customer.id is not None:
            existing = self.identity_map.get(Customer, customer.id)
            if existing:
                self.identity_map.remove(existing)
        
        customer_model = CustomerModel.from_entity(customer)
        
        person_model = None
        if customer.person.id is not None:
            person_model = self.db_session.query(PersonModel).get(customer.person.id)
        if not person_model:
            person_model = PersonModel.from_entity(customer.person)
        
        customer_model.person = person_model

        self.db_session.add(customer_model)
        self.db_session.commit()
        self.db_session.refresh(customer_model)

        return customer_model.to_entity()
    
    def get_by_id(self, customer_id: int) -> Customer:
        customer_model = (
            self.db_session.query(CustomerModel)
            .filter(CustomerModel.id == customer_id)
            .first()
        )
        if not customer_model:
            return None
        return customer_model.to_entity()
    
    def get_by_cpf(self, cpf: str) -> Customer:
        customer_model = (
            self.db_session.query(CustomerModel)
            .join(CustomerModel.person)
            .filter(PersonModel.cpf == cpf)
            .first()
        )
        if not customer_model:
            return None
        return customer_model.to_entity()
    
    def get_by_person_id(self, person_id: int) -> Customer:
        customer_model = (
            self.db_session.query(CustomerModel)
            .filter(CustomerModel.person_id == person_id)
            .first()
        )
        if not customer_model:
            return None
        return customer_model.to_entity()
    
    def get_all(self, include_deleted: bool = False) -> List[Customer]:
        query = self.db_session.query(CustomerModel)
        if not include_deleted:
            query = query.filter(CustomerModel.inactivated_at.is_(None))
        customer_models = query.all()
        return [cm.to_entity() for cm in customer_models]
    
    def update(self, customer: Customer) -> Customer:
        existing = self.identity_map.get(Customer, customer.id)
        if existing:
            self.identity_map.remove(existing)
        
        customer_model = CustomerModel.from_entity(customer)
        customer_model.person = PersonModel.from_entity(customer.person)

        self.db_session.merge(customer_model)
        self.db_session.commit()
        return self.get_by_id(customer_model.id)
    
    def delete(self, customer: Customer) -> None:
        customer_model = (
            self.db_session.query(CustomerModel)
            .filter(CustomerModel.id == customer.id)
            .first()
        )

        if customer_model:
            self.db_session.delete(customer_model)
            self.db_session.commit()
            self.identity_map.remove(customer)

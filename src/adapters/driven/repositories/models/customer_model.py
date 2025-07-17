
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.customer import Customer


class CustomerModel(BaseModel):
    __tablename__ = 'customers'

    person_id = Column(ForeignKey('persons.id'), nullable=True)
    person = relationship('PersonModel')    

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=getattr(entity, 'id', None),
            created_at=getattr(entity, 'created_at', None),
            updated_at=getattr(entity, 'updated_at', None),
            inactivated_at=getattr(entity, 'inactivated_at', None),
            person_id=entity.person.id
        )
    
    def to_entity(self):
        identity_map = IdentityMap.get_instance()

        existing = identity_map.get(Customer, self.id)
        if existing:
            return existing
        
        customer_entity = Customer(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
            person=self.person.to_entity()
        )
        identity_map.add(customer_entity)
        return customer_entity


__all__ = ['CustomerModel']

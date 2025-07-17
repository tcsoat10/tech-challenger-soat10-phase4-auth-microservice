from pydantic import BaseModel

from src.core.domain.dtos.person.person_dto import PersonDTO
from src.core.domain.entities.customer import Customer


class CustomerDTO(BaseModel):
    id: int
    person: PersonDTO

    @classmethod
    def from_entity(cls, customer: Customer) -> 'CustomerDTO':
        return cls(id=customer.id, person=PersonDTO.from_entity(customer.person))
    
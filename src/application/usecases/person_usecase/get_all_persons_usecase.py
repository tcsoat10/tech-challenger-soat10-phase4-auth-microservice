from src.core.ports.person.i_person_repository import IPersonRepository
from typing import Optional, List
from src.core.domain.entities.person import Person


class GetAllPersonsUsecase:
    def __init__(self, person_gateway: IPersonRepository):
        self.person_gateway = person_gateway

    @classmethod
    def build(cls, person_gateway: IPersonRepository) -> 'GetAllPersonsUsecase':
        return cls(person_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[Person]:
        persons = self.person_gateway.get_all(include_deleted)
        return persons
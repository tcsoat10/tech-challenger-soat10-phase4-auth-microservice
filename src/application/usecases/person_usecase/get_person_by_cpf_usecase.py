from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.domain.entities.person import Person
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException

class GetPersonByCpfUsecase:
    def __init__(self, person_gateway: IPersonRepository):
        self.person_gateway = person_gateway
    
    @classmethod
    def build(cls, person_gateway: IPersonRepository) -> 'GetPersonByCpfUsecase':
        return cls(person_gateway)
    
    def execute(self, cpf: str) -> Person:
        person = self.person_gateway.get_by_cpf(cpf)
        if not person:
            raise EntityNotFoundException(entity_name='Person')
        
        return person
    
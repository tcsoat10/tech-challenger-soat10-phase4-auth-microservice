from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeletePersonUsecase:
    def __init__(self, person_gateway: IPersonRepository):
        self.person_gateway = person_gateway

    @classmethod
    def build(cls, person_gateway: IPersonRepository) -> 'DeletePersonUsecase':
        return cls(person_gateway)
    
    def execute(self, person_id: int) -> None:
        person = self.person_gateway.get_by_id(person_id)
        if not person:
            raise EntityNotFoundException(entity_name='Person')
        
        if DELETE_MODE == 'soft':
            if person.is_deleted():
                raise EntityNotFoundException(entity_name='Person')
            
            person.soft_delete()
            self.person_gateway.update(person)
        
        else:
            self.person_gateway.delete(person)
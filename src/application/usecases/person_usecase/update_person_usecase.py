from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO
from src.core.domain.entities.person import Person
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class UpdatePersonUsecase:
    def __init__(self, person_gateway: IPersonRepository):
        self.person_gateway = person_gateway

    @classmethod
    def build(cls, person_gateway: IPersonRepository) -> 'UpdatePersonUsecase':
        return cls(person_gateway)
    
    def execute(self, person_id: int, dto: UpdatePersonDTO) -> Person:
        person = self.person_gateway.get_by_id(person_id)
        if not person:
            raise EntityNotFoundException(entity_name='Person')
        
        person.name = dto.name
        person.cpf = dto.cpf
        person.email = dto.email
        person.birth_date = dto.birth_date

        updated_person = self.person_gateway.update(person)

        return updated_person
    
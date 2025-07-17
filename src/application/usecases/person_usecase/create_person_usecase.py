from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.core.domain.entities.person import Person
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException


class CreatePersonUsecase:
    def __init__(self, person_gateway: IPersonRepository):
        self.person_gateway = person_gateway

    @classmethod
    def build(cls, person_gateway: IPersonRepository):
        return cls(person_gateway)
    
    def execute(self, dto: CreatePersonDTO) -> Person:
        person = self.person_gateway.get_by_cpf(dto.cpf)
        if person:
            if not person.is_deleted():
                raise EntityDuplicatedException(entity_name='Person')
            
            person.name = dto.name
            person.cpf = dto.cpf
            person.email = dto.email
            person.birth_date = dto.birth_date
            person.reactivate()
            self.person_gateway.update(person)
        
        else:
            person = Person(name=dto.name, cpf=dto.cpf, email=dto.email, birth_date=dto.birth_date)
            person = self.person_gateway.create(person)

        return person    
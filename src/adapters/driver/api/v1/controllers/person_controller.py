from typing import Optional, List

from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.core.domain.dtos.person.person_dto import PersonDTO
from src.application.usecases.person_usecase.create_person_usecase import CreatePersonUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.person_usecase.get_person_by_cpf_usecase import GetPersonByCpfUsecase
from src.application.usecases.person_usecase.get_person_by_id_usecase import GetPersonByIdUsecase
from src.application.usecases.person_usecase.get_all_persons_usecase import GetAllPersonsUsecase
from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO
from src.application.usecases.person_usecase.update_person_usecase import UpdatePersonUsecase
from src.application.usecases.person_usecase.delete_person_usecase import DeletePersonUsecase


class PersonController:
    
    def __init__(self, person_gateway: IPersonRepository):
        self.person_gateway: IPersonRepository = person_gateway

    def create_person(self, dto: CreatePersonDTO) -> PersonDTO:
        create_person_usecase = CreatePersonUsecase.build(self.person_gateway)
        person = create_person_usecase.execute(dto)
        return DTOPresenter.transform(person, PersonDTO)
    
    def get_person_by_cpf(self, cpf: str) -> PersonDTO:
        person_by_cpf_usecase = GetPersonByCpfUsecase.build(self.person_gateway)
        person = person_by_cpf_usecase.execute(cpf)
        return DTOPresenter.transform(person, PersonDTO)
    
    def get_person_by_id(self, person_id: int) -> PersonDTO:
        person_by_id_usecase = GetPersonByIdUsecase.build(self.person_gateway)
        person = person_by_id_usecase.execute(person_id)
        return DTOPresenter.transform(person, PersonDTO)
    
    def get_all_persons(self, include_deleted: Optional[bool] = False) -> List[PersonDTO]:
        all_persons_usecase = GetAllPersonsUsecase.build(self.person_gateway)
        persons = all_persons_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(persons, PersonDTO)
    
    def update_person(self, person_id: int, dto: UpdatePersonDTO) -> PersonDTO:
        update_person_usecase = UpdatePersonUsecase.build(self.person_gateway)
        person = update_person_usecase.execute(person_id, dto)
        return DTOPresenter.transform(person, PersonDTO)
    
    def delete_person(self, person_id: int) -> None:
        delete_person_usecase = DeletePersonUsecase.build(self.person_gateway)
        delete_person_usecase.execute(person_id)
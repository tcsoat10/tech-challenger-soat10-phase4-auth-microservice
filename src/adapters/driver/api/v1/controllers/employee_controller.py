
from typing import Optional

from src.application.usecases.employee_usecase.delete_employee_usecase import DeleteEmployeeUseCase
from src.application.usecases.employee_usecase.update_employee_usecase import UpdateEmployeeUseCase
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO
from src.application.usecases.employee_usecase.get_all_employees_usecase import GetAllEmployeesUseCase
from src.application.usecases.employee_usecase.list_employees_by_role_id import ListEmployeesByRoleIdUseCase
from src.application.usecases.employee_usecase.get_employee_by_user_id_usecase import GetEmployeeByUserIdUseCase
from src.application.usecases.employee_usecase.get_employee_by_person_id_usecase import GetEmployeeByPersonIdUseCase
from src.application.usecases.employee_usecase.get_employee_by_id_usecase import GetEmployeeByIdUseCase
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.application.usecases.employee_usecase.create_employee_usecase import CreateEmployeeUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.ports.employee.i_employee_repository import IEmployeeRepository

class EmployeeController:
    
    def __init__(
        self, 
        employee_gateway: IEmployeeRepository, 
        person_gateway: IPersonRepository, 
        role_gateway: IRoleRepository, 
        user_gateway: IUserRepository
    ):
        self.employee_gateway = employee_gateway
        self.person_gateway = person_gateway
        self.role_gateway = role_gateway
        self.user_gateway = user_gateway
        
    def create_employee(self, dto: CreateEmployeeDTO) -> EmployeeDTO:
        create_employee_use_case = CreateEmployeeUseCase.build(
            self.employee_gateway,
            self.person_gateway,
            self.role_gateway,
            self.user_gateway
        )
        employee = create_employee_use_case.execute(dto)
        return DTOPresenter.transform(employee, EmployeeDTO)

    def get_employee_by_id(self, employee_id: int) -> EmployeeDTO:
        get_employee_by_id_use_case = GetEmployeeByIdUseCase.build(self.employee_gateway)
        employee = get_employee_by_id_use_case.execute(employee_id)
        return DTOPresenter.transform(employee, EmployeeDTO)
    
    def get_employee_by_person_id(self, person_id: int) -> EmployeeDTO:
        get_employee_by_person_id_use_case = GetEmployeeByPersonIdUseCase.build(self.employee_gateway)
        employee = get_employee_by_person_id_use_case.execute(person_id)
        return DTOPresenter.transform(employee, EmployeeDTO)

    def get_employee_by_user_id(self, user_id: int) -> EmployeeDTO:
        get_employee_by_user_id_use_case = GetEmployeeByUserIdUseCase.build(self.employee_gateway)
        employee = get_employee_by_user_id_use_case.execute(user_id)
        return DTOPresenter.transform(employee, EmployeeDTO)

    def list_employees_by_role_id(self, role_id: int) -> list[EmployeeDTO]:
        list_employees_by_role_id_use_case = ListEmployeesByRoleIdUseCase.build(self.employee_gateway)
        employees = list_employees_by_role_id_use_case.execute(role_id)
        return DTOPresenter.transform_list(employees, EmployeeDTO)

    def get_all_employees(self, include_deleted: Optional[bool] = False) -> list[EmployeeDTO]:
        get_all_employees_use_case = GetAllEmployeesUseCase.build(self.employee_gateway)
        employees = get_all_employees_use_case.execute(include_deleted=include_deleted)
        return DTOPresenter.transform_list(employees, EmployeeDTO)

    def update_employee(self, employee_id: int, dto: UpdateEmployeeDTO) -> EmployeeDTO:
        update_employee_use_case = UpdateEmployeeUseCase.build(
            self.employee_gateway,
            self.person_gateway,
            self.role_gateway,
            self.user_gateway,
        )
        employee = update_employee_use_case.execute(employee_id, dto)
        return DTOPresenter.transform(employee, EmployeeDTO)
    
    def delete_employee(self, employee_id: int) -> None:
        delete_employee_use_case = DeleteEmployeeUseCase.build(self.employee_gateway)
        delete_employee_use_case.execute(employee_id)
        return None

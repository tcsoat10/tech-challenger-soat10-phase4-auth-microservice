
from typing import Optional
from src.core.domain.entities.employee import Employee
from src.core.ports.employee.i_employee_repository import IEmployeeRepository


class GetAllEmployeesUseCase:
    
    def __init__(self, employee_gateway: IEmployeeRepository):
        self.employee_gateway = employee_gateway
        
    @classmethod
    def build(cls, employee_gateway: IEmployeeRepository) -> 'GetAllEmployeesUseCase':
        return cls(employee_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> list[Employee]:
        employees = self.employee_gateway.get_all(include_deleted=include_deleted)
        return employees

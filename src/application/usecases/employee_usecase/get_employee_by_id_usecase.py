
from src.core.domain.entities.employee import Employee
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.employee.i_employee_repository import IEmployeeRepository


class GetEmployeeByIdUseCase:
    
    def __init__(self, employee_gateway: IEmployeeRepository):
        self.employee_gateway = employee_gateway
        
    @classmethod
    def build(cls, employee_gateway: IEmployeeRepository) -> 'GetEmployeeByIdUseCase':
        return cls(employee_gateway)
    
    def execute(self, employee_id: int) -> Employee:
        employee = self.employee_gateway.get_by_id(employee_id=employee_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')

        return employee

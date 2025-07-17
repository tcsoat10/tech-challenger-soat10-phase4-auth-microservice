
from src.core.domain.entities.employee import Employee
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.employee.i_employee_repository import IEmployeeRepository


class GetEmployeeByUserIdUseCase:
    
    def __init__(self, employee_gateway: IEmployeeRepository):
        self.employee_gateway = employee_gateway
        
    @classmethod
    def build(cls, employee_gateway: IEmployeeRepository) -> 'GetEmployeeByUserIdUseCase':
        return cls(employee_gateway)
    
    def execute(self, user_id: int) -> Employee:
        employee = self.employee_gateway.get_by_user_id(user_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')

        return employee

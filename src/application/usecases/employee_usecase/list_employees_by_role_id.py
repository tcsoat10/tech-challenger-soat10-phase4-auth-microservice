
from src.core.domain.entities.employee import Employee
from src.core.ports.employee.i_employee_repository import IEmployeeRepository


class ListEmployeesByRoleIdUseCase:
    
    def __init__(self, employee_gateway: IEmployeeRepository):
        self.employee_gateway = employee_gateway
        
    @classmethod
    def build(cls, employee_gateway: IEmployeeRepository) -> 'ListEmployeesByRoleIdUseCase':
        return cls(employee_gateway)
    
    def execute(self, role_id: int) -> list[Employee]:
        employees = self.employee_gateway.get_by_role_id(role_id)
        return employees

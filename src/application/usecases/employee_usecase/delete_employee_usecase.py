
from config.database import DELETE_MODE
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.employee.i_employee_repository import IEmployeeRepository


class DeleteEmployeeUseCase:
    
    def __init__(self, employee_gateway: IEmployeeRepository):
        self.employee_gateway = employee_gateway
    
    @classmethod
    def build(cls, employee_gateway: IEmployeeRepository) -> 'DeleteEmployeeUseCase':
        return cls(employee_gateway)
    
    def execute(self, employee_id: int) -> None:
        employee = self.employee_gateway.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')
        
        if DELETE_MODE == 'soft':
            if employee.is_deleted():
                raise EntityNotFoundException(entity_name='Employee')
            employee.soft_delete()
            self.employee_gateway.update(employee)
        else:
            self.employee_gateway.delete(employee_id)

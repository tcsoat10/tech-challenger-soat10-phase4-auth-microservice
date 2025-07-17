from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeleteRoleUsecase:
    def __init__(self, role_gateway: IRoleRepository):
        self.role_gateway = role_gateway

    @classmethod
    def build(cls, role_gateway: IRoleRepository) -> 'DeleteRoleUsecase':
        return cls(role_gateway)
    
    def execute(self, role_id: int) -> None:
        role = self.role_gateway.get_by_id(role_id)
        if not role:
            raise EntityNotFoundException(entity_name='Role')
        
        if DELETE_MODE == 'soft':
            if role.is_deleted():
                
                raise EntityNotFoundException(entity_name='Role')
            role.soft_delete()
            self.role_gateway.update(role)
        else:
            self.role_gateway.delete(role)
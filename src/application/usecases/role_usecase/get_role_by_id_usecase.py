from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.entities.role import Role
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class GetRoleByIdUsecase:
    def __init__(self, role_gateway: IRoleRepository):
        self.role_gateway = role_gateway

    @classmethod
    def build(cls, role_gateway: IRoleRepository) -> 'GetRoleByIdUsecase':
        return cls(role_gateway)
    
    def exexute(self, role_id: int) -> Role:
        role = self.role_gateway.get_by_id(role_id)
        if not role:
            raise EntityNotFoundException(entity_name='Role')
        
        return role
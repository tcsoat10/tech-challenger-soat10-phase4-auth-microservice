from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.entities.role import Role
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class UpdateRoleUsecase:
    def __init__(self, role_gateway: IRoleRepository):
        self.role_gateway = role_gateway

    @classmethod
    def build(cls, role_gateway: IRoleRepository) -> 'UpdateRoleUsecase':
        return cls(role_gateway)
    
    def execute(self, role_id: int, dto: UpdateRoleDTO) -> Role:
        role = self.role_gateway.get_by_id(role_id)
        if not role:
            raise EntityNotFoundException(entity_name='Role')
        
        role.name = dto.name
        role.description = dto.description
        role = self.role_gateway.update(role)

        return role
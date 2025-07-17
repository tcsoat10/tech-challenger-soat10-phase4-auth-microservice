from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.entities.role import Role
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException


class CreateRoleUsecase:
    def __init__(self, role_gateway: IRoleRepository):
        self.role_gateway = role_gateway

    @classmethod
    def build(cls, role_gateway: IRoleRepository) -> 'CreateRoleUsecase':
        return cls(role_gateway)
    
    def execute(self, dto: CreateRoleDTO) -> Role:
        role = self.role_gateway.get_by_name(dto.name)
        if role:
            if not role.is_deleted():
                raise EntityDuplicatedException(entity_name='Role')
            
            role.name = dto.name
            role.description = dto.description
            role.reactivate()
            self.role_gateway.update(role)
        
        else:
            role = Role(name=dto.name, description=dto.description)
            role = self.role_gateway.create(role)

        return role
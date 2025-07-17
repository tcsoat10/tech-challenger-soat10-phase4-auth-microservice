from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.domain.entities.permission import Permission
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException


class CreatePermissionUsecase:
    def __init__(self, permission_gateway: IPermissionRepository):
        self.permission_gateway = permission_gateway

    @classmethod
    def build(cls, permission_gateway: IPermissionRepository):
        return cls(permission_gateway)
    
    def execute(self, dto: CreatePermissionDTO) -> Permission:
        permission = self.permission_gateway.get_by_name(dto.name)
        if permission:
            if not permission.is_deleted():
                raise EntityDuplicatedException(entity_name='Permission')
            
            permission.name = dto.name
            permission.description = dto.description
            permission.reactivate()
            self.permission_gateway.update(permission)

        else:
            permission = Permission(name=dto.name, description=dto.description)
            permission = self.permission_gateway.create(permission)

        return permission
    
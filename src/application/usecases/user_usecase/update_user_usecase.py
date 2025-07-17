from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO
from src.core.domain.entities.user import User
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class UpdateUserUsecase:
    def __init__(self, user_gateway: IUserRepository):
        self.user_gateway = user_gateway

    @classmethod
    def build(cls, user_gateway: IUserRepository) -> 'UpdateUserUsecase':
        return cls(user_gateway)
    
    def execute(self, user_id: int, dto: UpdateUserDTO) -> User:
        user = self.user_gateway.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException(entity_name='User')
        
        user.name = dto.name
        user.password = dto.password
        updated_user = self.user_gateway.update(user)

        return updated_user
    
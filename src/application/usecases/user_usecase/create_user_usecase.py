from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.entities.user import User
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException


class CreateUserUsecase:
    def __init__(self, user_gateway: IUserRepository):
        self.user_gateway = user_gateway

    @classmethod
    def build(cls, user_gateway: IUserRepository) -> 'CreateUserUsecase':
        return cls(user_gateway)
    
    def execute(self, dto: CreateUserDTO) -> User:
        user = self.user_gateway.get_by_name(dto.name)
        if user:
            if not user.is_deleted():
                raise EntityDuplicatedException(entity_name='User')
            
            user.name = dto.name
            user.password = dto.password
            user.reactivate()
            self.user_gateway.update(user)
        else:
            user = User(name=dto.name, password=dto.password)
            user = self.user_gateway.create(user)
        
        return user

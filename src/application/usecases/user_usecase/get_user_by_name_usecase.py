from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.entities.user import User
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException



class GetUserByNameUsecase:
    def __init__(self, user_gateway: IUserRepository):
        self.user_gateway = user_gateway

    @classmethod
    def build(cls, user_gateway: IUserRepository):
        return cls(user_gateway)
    
    def execute(self, name: str) -> User:
        user = self.user_gateway.get_by_name(name=name)
        if not user:
            raise EntityNotFoundException(entity_name='User')
        
        return user
    
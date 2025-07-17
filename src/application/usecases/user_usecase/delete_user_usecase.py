from src.core.ports.user.i_user_repository import IUserRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from config.database import DELETE_MODE


class DeleteUserUsecase:
    def __init__(self, user_gateway: IUserRepository):
        self.user_gateway = user_gateway

    @classmethod
    def build(cls, user_gateway: IUserRepository) -> 'DeleteUserUsecase':
        return cls(user_gateway)
    
    def execute(self, user_id: int) -> None:
        user = self.user_gateway.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException(entity_name='User')
        
        if DELETE_MODE == 'soft':
            if user.is_deleted():
                raise EntityNotFoundException(entity_name='User')
            
            user.soft_delete()
            self.user_gateway.update(user)
        else:
            self.user_gateway.delete(user)
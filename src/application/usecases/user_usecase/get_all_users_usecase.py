from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.entities.user import User

from typing import Optional, List


class GetAllUsersUsecase:
    def __init__(self, user_gateway: IUserRepository):
        self.user_gateway = user_gateway

    @classmethod
    def build(cls, user_gateway: IUserRepository):
        return cls(user_gateway)
    
    def execute(self, include_deleted: Optional[bool] = False) -> List[User]:
        users = self.user_gateway.get_all(include_deleted=include_deleted)
        return users
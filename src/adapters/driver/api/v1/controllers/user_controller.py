from typing import Optional, List

from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.user_dto import UserDTO
from src.application.usecases.user_usecase.create_user_usecase import CreateUserUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.user_usecase.get_user_by_name_usecase import GetUserByNameUsecase
from src.application.usecases.user_usecase.get_user_by_id_usecase import GetUserByIdUsecase
from src.application.usecases.user_usecase.get_all_users_usecase import GetAllUsersUsecase
from src.application.usecases.user_usecase.update_user_usecase import UpdateUserUsecase
from src.application.usecases.user_usecase.delete_user_usecase import DeleteUserUsecase


class UserController:
    
    def __init__(self, user_gateway: IUserRepository):
        self.user_gateway: IUserRepository = user_gateway
    
    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        create_user_usecase = CreateUserUsecase.build(self.user_gateway)
        user = create_user_usecase.execute(dto)
        return DTOPresenter.transform(user, UserDTO)
    
    def get_user_by_name(self, name: str) -> UserDTO:
        user_by_name_usecase = GetUserByNameUsecase.build(self.user_gateway)
        user = user_by_name_usecase.execute(name)
        return DTOPresenter.transform(user, UserDTO)
    
    def get_user_by_id(self, user_id: int) -> UserDTO:
        user_by_id_usecase = GetUserByIdUsecase.build(self.user_gateway)
        user = user_by_id_usecase.execute(user_id)
        return DTOPresenter.transform(user, UserDTO)
    
    def get_all_users(self, include_deleted: Optional[bool]) -> List[UserDTO]:
        all_users_usecase = GetAllUsersUsecase.build(self.user_gateway)
        users = all_users_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(users, UserDTO)

    def update_user(self, user_id: int, dto: CreateUserDTO) -> UserDTO:
        update_user_usecase = UpdateUserUsecase.build(self.user_gateway)
        user = update_user_usecase.execute(user_id, dto)
        return DTOPresenter.transform(user, UserDTO)
    
    def delete_user(self, user_id: int) -> None:
        delete_user_usecase = DeleteUserUsecase.build(self.user_gateway)
        delete_user_usecase.execute(user_id)

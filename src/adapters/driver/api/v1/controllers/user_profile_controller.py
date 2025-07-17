from typing import Optional, List

from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.dtos.user_profile.user_profile_dto import UserProfileDTO
from src.application.usecases.user_profile_usecase.create_user_profile_usecase import CreateUserProfileUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.user_profile_usecase.get_user_profile_by_id_usecase import GetUserProfileByIdUsecase
from src.application.usecases.user_profile_usecase.get_user_profile_by_user_id_and_profile_id_usecase import GetUserProfileByUserIdAndProfileIdUsecase
from src.application.usecases.user_profile_usecase.get_all_user_profiles_usecase import GetAllUserProfilesUsecase
from src.core.domain.dtos.user_profile.update_user_profile_dto import UpdateUserProfileDTO
from src.application.usecases.user_profile_usecase.update_user_profile_usecase import UpdateUserProfileUsecase
from src.application.usecases.user_profile_usecase.delete_user_profile_usecase import DeleteUserProfileUsecase


class UserProfileController:
    
    def __init__(self, user_profile_gateway: IUserProfileRepository, profile_gateway: IProfileRepository, user_gateway: IUserRepository) -> None:
        self.user_profile_gateway: IUserProfileRepository = user_profile_gateway
        self.profile_gateway: IProfileRepository = profile_gateway
        self.user_gateway: IUserRepository = user_gateway

    def create_user_profile(self, dto: CreateUserProfileDTO) -> UserProfileDTO:
        create_user_profile_usecase = CreateUserProfileUsecase.build(
            self.user_profile_gateway, self.profile_gateway, self.user_gateway
        )
        user_profile = create_user_profile_usecase.execute(dto)
        return DTOPresenter.transform(user_profile, UserProfileDTO)
    
    def get_user_profile_by_id(self, user_profile_id: int) -> UserProfileDTO:
        get_user_profile_by_id_usecase = GetUserProfileByIdUsecase.build(self.user_profile_gateway)
        user_profile = get_user_profile_by_id_usecase.execute(user_profile_id)
        return DTOPresenter.transform(user_profile, UserProfileDTO)
    
    def get_user_profile_by_user_id_and_profile_id(self, user_id: int, profile_id: int) -> UserProfileDTO:
        user_profile_by_user_id_and_profile_id_usecase = GetUserProfileByUserIdAndProfileIdUsecase.build(
            self.user_profile_gateway
        )
        user_profile = user_profile_by_user_id_and_profile_id_usecase.execute(user_id, profile_id)
        return DTOPresenter.transform(user_profile, UserProfileDTO)

    def get_all_user_profiles(self, include_deleted: Optional[bool] = False) -> List[UserProfileDTO]:
        all_user_profiles_usecase = GetAllUserProfilesUsecase.build(self.user_profile_gateway)
        user_profiles = all_user_profiles_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(user_profiles, UserProfileDTO)
    
    def update_user_profile(self, user_profile_id, dto: UpdateUserProfileDTO) -> UserProfileDTO:
        update_user_profile_usecase = UpdateUserProfileUsecase.build(
            self.user_profile_gateway, self.profile_gateway, self.user_gateway
        )
        user_profile = update_user_profile_usecase.execute(user_profile_id, dto)
        return DTOPresenter.transform(user_profile, UserProfileDTO)
    
    def delete_user_profile(self, user_profile_id) -> None:
        delete_user_profile_usecase = DeleteUserProfileUsecase.build(self.user_profile_gateway)
        delete_user_profile_usecase.execute(user_profile_id)
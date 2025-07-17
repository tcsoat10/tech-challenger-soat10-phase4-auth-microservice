from typing import List, Optional

from src.application.usecases.profile_usecase.delete_profile_usecase import DeleteProfileUsecase
from src.application.usecases.profile_usecase.update_profile_usecase import UpdateProfileUsecase
from src.application.usecases.profile_usecase.get_all_profiles_usecase import GetAllProfilesUsecase
from src.application.usecases.profile_usecase.get_profile_by_id_usecase import GetProfileByIdUsecase
from src.application.usecases.profile_usecase.get_profile_by_name_usecase import GetProfileByNameUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.application.usecases.profile_usecase.create_profile_usecase import CreateProfileUsecase


class ProfileController:
    
    def __init__(self, profile_gateway: IProfileRepository):
        self.profile_gateway: IProfileRepository = profile_gateway

    def create_profile(self, dto: CreateProfileDTO) -> ProfileDTO:
        create_profile_usecase = CreateProfileUsecase.build(self.profile_gateway)
        profile = create_profile_usecase.execute(dto)
        return DTOPresenter.transform(profile, ProfileDTO)
    
    def get_profile_by_name(self, name: str) -> ProfileDTO:
        profile_by_name_usecase = GetProfileByNameUseCase.build(self.profile_gateway)
        profile = profile_by_name_usecase.execute(name)
        return DTOPresenter.transform(profile, ProfileDTO)
    
    def get_profile_by_id(self, profile_id: int) -> ProfileDTO:
        profile_by_id_usecase = GetProfileByIdUsecase.build(self.profile_gateway)
        profile = profile_by_id_usecase.execute(profile_id)
        return DTOPresenter.transform(profile, ProfileDTO)
    
    def get_all_profiles(self, include_deleted: Optional[bool]) -> List[ProfileDTO]:
        all_profiles_usecase = GetAllProfilesUsecase.build(self.profile_gateway)
        profiles = all_profiles_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(profiles, ProfileDTO)
    
    def update_profile(self, profile_id: int, dto: CreateProfileDTO) -> ProfileDTO:
        update_profile_usecase = UpdateProfileUsecase.build(self.profile_gateway)
        profile = update_profile_usecase.execute(profile_id, dto)
        return DTOPresenter.transform(profile, ProfileDTO)
    
    def delete_profile(self, profile_id: int) -> None:
        delete_profile_usecase = DeleteProfileUsecase.build(self.profile_gateway)
        delete_profile_usecase.execute(profile_id)
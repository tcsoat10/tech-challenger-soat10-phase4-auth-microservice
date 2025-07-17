import pytest
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.domain.dtos.profile.update_profile_dto import UpdateProfileDTO
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.application.usecases.profile_usecase.create_profile_usecase import CreateProfileUsecase
from src.application.usecases.profile_usecase.get_all_profiles_usecase import GetAllProfilesUsecase
from src.application.usecases.profile_usecase.delete_profile_usecase import DeleteProfileUsecase
from src.application.usecases.profile_usecase.update_profile_usecase import UpdateProfileUsecase


class TestProfileUsecases:
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.profile_gateway = ProfileRepository(db_session)
        self.create_profile_usecase = CreateProfileUsecase(self.profile_gateway)
        self.get_all_profiles_usecase = GetAllProfilesUsecase(self.profile_gateway)
        self.delete_profile_usecase = DeleteProfileUsecase(self.profile_gateway)
        self.update_profile_usecase = UpdateProfileUsecase(self.profile_gateway)
        
    def test_create_profile_usecase(self):
        dto = CreateProfileDTO(name='customer', description='Customer profile')
        profile = self.create_profile_usecase.execute(dto)

        assert profile.id is not None
        assert profile.name == 'customer'
        assert profile.description == 'Customer profile'

    def test_create_duplicate_profile_usecase(self):
        dto = CreateProfileDTO(name='customer', description='Customer profile')
        self.create_profile_usecase.execute(dto)

        with pytest.raises(EntityDuplicatedException):
            self.create_profile_usecase.execute(dto)

    def test_get_all_profiles_usecase(self):
        dto1 = CreateProfileDTO(name='customer', description='Customer profile')
        dto2 = CreateProfileDTO(name='employee', description='Employee profile')

        self.create_profile_usecase.execute(dto1)
        self.create_profile_usecase.execute(dto2)

        profiles = self.get_all_profiles_usecase.execute()
        assert len(profiles) == 2
        assert profiles[0].name == 'customer'
        assert profiles[1].name == 'employee'

    def test_delete_profile_usecase(self):
        dto = CreateProfileDTO(name='customer', description='Customer profile')
        profile = self.create_profile_usecase.execute(dto)

        self.delete_profile_usecase.execute(profile.id)
        assert profile.is_deleted() is True

    def test_update_profile_usecase(self):
        create_dto = CreateProfileDTO(name='customer', description='Customer profile')
        profile = self.create_profile_usecase.execute(create_dto)

        update_dto = UpdateProfileDTO(id=profile.id, name='updated_customer', description='Updated customer profile')
        updated_profile = self.update_profile_usecase.execute(profile.id, update_dto)

        assert updated_profile.name == 'updated_customer'
        assert updated_profile.description == 'Updated customer profile'

    def test_update_profile_not_found_usecase(self):
        update_dto = UpdateProfileDTO(id=1, name='updated_customer', description='Updated customer profile')
        
        with pytest.raises(EntityNotFoundException):
            self.update_profile_usecase.execute(1, update_dto)

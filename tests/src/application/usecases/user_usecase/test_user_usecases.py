import pytest
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO
from src.adapters.driven.repositories.user_repository import UserRepository
from src.application.usecases.user_usecase.create_user_usecase import CreateUserUsecase
from src.application.usecases.user_usecase.get_all_users_usecase import GetAllUsersUsecase
from src.application.usecases.user_usecase.delete_user_usecase import DeleteUserUsecase
from src.application.usecases.user_usecase.update_user_usecase import UpdateUserUsecase


class TestUserUsecases:
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.user_gateway = UserRepository(db_session)
        self.create_user_usecase = CreateUserUsecase(self.user_gateway)
        self.get_all_users_usecase = GetAllUsersUsecase(self.user_gateway)
        self.delete_user_usecase = DeleteUserUsecase(self.user_gateway)
        self.update_user_usecase = UpdateUserUsecase(self.user_gateway)
    
    def test_create_user_usecase(self):
        dto = CreateUserDTO(name='testuser', password='testpass123')
        user = self.create_user_usecase.execute(dto)

        assert user.id is not None
        assert user.name == 'testuser'
        assert user.verify_password('testpass123')

    def test_create_duplicate_user_usecase(self):
        dto = CreateUserDTO(name='testuser', password='testpass123')
        self.create_user_usecase.execute(dto)

        with pytest.raises(EntityDuplicatedException):
            self.create_user_usecase.execute(dto)

    def test_get_all_users_usecase(self):
        dto1 = CreateUserDTO(name='testuser1', password='testpass123')
        dto2 = CreateUserDTO(name='testuser2', password='testpass123')

        self.create_user_usecase.execute(dto1)
        self.create_user_usecase.execute(dto2)

        users = self.get_all_users_usecase.execute()
        assert len(users) == 2
        assert users[0].name == 'testuser1'
        assert users[1].name == 'testuser2'

    def test_delete_user_usecase(self):
        dto = CreateUserDTO(name='testuser', password='testpass123')
        user = self.create_user_usecase.execute(dto)

        self.delete_user_usecase.execute(user.id)
        assert user.is_deleted() is True

    def test_update_user_usecase(self):
        create_dto = CreateUserDTO(name='testuser', password='testpass123')
        user = self.create_user_usecase.execute(create_dto)

        update_dto = UpdateUserDTO(id=user.id, name='updateduser', password='newpass123')
        updated_user = self.update_user_usecase.execute(user.id, update_dto)

        assert updated_user.name == 'updateduser'
        assert updated_user.verify_password('newpass123')

    def test_update_user_not_found_usecase(self):
        update_dto = UpdateUserDTO(id=1, name='updateduser', password='newpass123')
        
        with pytest.raises(EntityNotFoundException):
            self.update_user_usecase.execute(1, update_dto)

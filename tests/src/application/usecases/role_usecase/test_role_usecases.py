import pytest
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.application.usecases.role_usecase.create_role_usecase import CreateRoleUsecase
from src.application.usecases.role_usecase.get_all_roles_usecase import GetAllRolesUsecase
from src.application.usecases.role_usecase.delete_role_usecase import DeleteRoleUsecase
from src.application.usecases.role_usecase.update_role_usecase import UpdateRoleUsecase

class TestRoleUsecases:
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.role_gateway = RoleRepository(db_session)
        self.create_role_usecase = CreateRoleUsecase(self.role_gateway)
        self.get_all_roles_usecase = GetAllRolesUsecase(self.role_gateway)
        self.delete_role_usecase = DeleteRoleUsecase(self.role_gateway)
        self.update_role_usecase = UpdateRoleUsecase(self.role_gateway)
    
    def test_create_role_usecase(self):
        dto = CreateRoleDTO(name='manager', description='Manager role')
        role = self.create_role_usecase.execute(dto)

        assert role.id is not None
        assert role.name == 'manager'
        assert role.description == 'Manager role'

    def test_create_duplicate_role_usecase(self):
        dto = CreateRoleDTO(name='manager', description='Manager role')
        self.create_role_usecase.execute(dto)

        with pytest.raises(EntityDuplicatedException):
            self.create_role_usecase.execute(dto)

    def test_get_all_roles_usecase(self):
        dto1 = CreateRoleDTO(name='manager', description='Manager role')
        dto2 = CreateRoleDTO(name='cashier', description='Cashier role')

        self.create_role_usecase.execute(dto1)
        self.create_role_usecase.execute(dto2)

        roles = self.get_all_roles_usecase.execute()
        assert len(roles) == 2
        assert roles[0].name == 'manager'
        assert roles[1].name == 'cashier'

    def test_delete_role_usecase(self):
        dto = CreateRoleDTO(name='manager', description='Manager role')
        role = self.create_role_usecase.execute(dto)

        self.delete_role_usecase.execute(role.id)
        
        role = self.role_gateway.get_by_id(role.id)
        assert role.is_deleted() is True

    def test_update_role_usecase(self):
        create_dto = CreateRoleDTO(name='manager', description='Manager role')
        role = self.create_role_usecase.execute(create_dto)

        update_dto = UpdateRoleDTO(id=role.id, name='head_manager', description='Head manager role')
        updated_role = self.update_role_usecase.execute(role.id, update_dto)

        assert updated_role.name == 'head_manager'
        assert updated_role.description == 'Head manager role'

    def test_update_role_not_found_usecase(self):
        update_dto = UpdateRoleDTO(id=1, name='head_manager', description='Head manager role')
        
        with pytest.raises(EntityNotFoundException):
            self.update_role_usecase.execute(1, update_dto)

import pytest
from src.adapters.driven.repositories.models.permission_model import PermissionModel
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.core.domain.entities.permission import Permission
from sqlalchemy.exc import IntegrityError
from tests.factories.permission_factory import PermissionFactory


class TestPermissionRepository:
    """
    Testes para o repositório de Permission.
    """
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = PermissionRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(PermissionModel).delete()
        self.db_session.commit()

    def test_create_permission_success(self):
        # Criando a permissão "Admin"
        admin_permission = Permission(name="Admin", description="System admin privileges")
        created_admin_permission = self.repository.create(admin_permission)

        assert created_admin_permission.id is not None
        assert created_admin_permission.name == "Admin"
        assert created_admin_permission.description == "System admin privileges"

        # Criando a permissão "Employee"
        employee_permission = Permission(name="Employee", description="System user privileges")
        created_employee_permission = self.repository.create(employee_permission)

        assert created_employee_permission.id is not None
        assert created_employee_permission.name == "Employee"
        assert created_employee_permission.description == "System user privileges"

        # Verifica se a permissão Admin foi persistida no banco
        db_permission = self.db_session.query(PermissionModel).filter_by(name="Admin").first()
        assert db_permission is not None
        assert db_permission.name == "Admin"

        # Verifica se a permissão Employee foi persistida no banco
        db_permission = self.db_session.query(PermissionModel).filter_by(name="Employee").first()
        assert db_permission is not None
        assert db_permission.name == "Employee"
    
    def test_create_duplicate_permission_return_error(self, db_session):
        '''
        Testa erro ao criar uma permissão com o nome duplicado
        '''

        # Criando a primeira permissão
        new_permission = Permission(name="Admin", description="System admin privileges")
        self.repository.create(new_permission)

        # Tentando criar a permissão duplicada
        duplicate_permission = Permission(name="Admin", description="New one")
        with pytest.raises(IntegrityError):
            self.repository.create(duplicate_permission)

    def test_get_permission_by_name_success(self):
        '''
        Testa a recuperação de uma permissão pelo nome com sucesso
        '''

        # Criando a primeira permissão
        new_permission = Permission(name="Admin", description="System admin privileges")
        created_permission = self.repository.create(new_permission)

        permission = self.repository.get_by_name(created_permission.name)

        assert permission is not None
        assert permission.id == created_permission.id
        assert permission.name == created_permission.name
        assert permission.description == created_permission.description

    def test_get_permission_by_name_with_name_not_registered(self):
        '''
        Testa a busca de uma permissão com um nome que não está registrado
        '''

        # Criando a primeira permissão
        new_permission = Permission(name="Admin", description="System admin privileges")
        self.repository.create(new_permission)

        permission = self.repository.get_by_name('not a name')

        assert permission is None
    
    def test_get_permission_by_id_success(self):
        '''
        Testa a recuperação de uma permissão pelo id
        '''

        # Criando a primeira permissão
        new_permission = Permission(name="Admin", description="System admin privileges")
        created_permission = self.repository.create(new_permission)

        permission = self.repository.get_by_id(created_permission.id)

        assert permission is not None
        assert permission.id == created_permission.id
        assert permission.name == created_permission.name
        assert permission.description == created_permission.description

    def test_get_permission_by_id_with_id_not_registered(self):
        '''
        Testa a busca de uma permissão com um id não registrado
        '''

        # Criando a primeira permissão
        new_permission = Permission(name="Admin", description="System admin privileges")
        self.repository.create(new_permission)

        permission = self.repository.get_by_id(2)

        assert permission is None
    
    def test_get_all_permissions(self):
        '''
        Testa a busca de todas as permissões
        '''

        # Criando as permissões
        permission1 = Permission(name="Admin", description="System admin privileges")
        permission2 = Permission(name="Employee", description="System user privileges")

        self.repository.create(permission1)
        self.repository.create(permission2)

        permissions = self.repository.get_all()

        assert len(permissions) == 2
        assert permissions[0].name == 'Admin'
        assert permissions[1].name == 'Employee'
    
    def test_get_all_permissions_with_empty_db(self):
        '''
        Testa a busca de todas as permissões com o banco de dados vazio
        '''

        permissions = self.repository.get_all()
        assert len(permissions) == 0
        assert permissions == []
    
    def test_update_permission(self):
        '''
        Testa a atualização de uma permissão
        '''

        permission = Permission(name="Admin", description="System admin privileges")
        created_permission = self.repository.create(permission)

        created_permission.name = 'Admin - updated'
        created_permission.description = 'System admin privileges - updated'

        updated_permission = self.repository.update(created_permission)

        assert updated_permission.name == created_permission.name
        assert updated_permission.description == created_permission.description

    def test_delete_permission(self):
        '''
        Testa a deleção de uma permissão
        '''
        
        permission = PermissionFactory()
        self.repository.delete(permission)

        assert len(self.repository.get_all()) == 0

    def test_delete_permission_with_inexistent_id(self):
        permission = PermissionFactory()
        unregistered_permission = Permission(name='test_permission', description='not_in_db')

        self.repository.delete(unregistered_permission)

        permissions = self.repository.get_all()
        assert len(permissions) == 1
        assert permissions[0].id == permission.id
        assert permissions[0].name == permission.name
        assert permissions[0].description == permission.description
        
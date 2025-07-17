import pytest
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.core.domain.entities.profile import Profile
from src.adapters.driven.repositories.models.profile_model import ProfileModel
from sqlalchemy.exc import IntegrityError


class TestProfileRepository:
    """
    Testes para o repositório de Profile.
    """
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = ProfileRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(ProfileModel).delete()
        self.db_session.commit()

    def test_create_profile_success(self):
        # Criando o perfil "Manager"
        manager_profile = Profile(name="Manager", description="Store manager")
        created_manager_profile = self.repository.create(manager_profile)

        assert created_manager_profile.id is not None
        assert created_manager_profile.name == "Manager"
        assert created_manager_profile.description == "Store manager"

        # Criando o perfil "Assistant"
        assistant_profile = Profile(name="Assistant", description="Store worker")
        created_assistant_profile = self.repository.create(assistant_profile)

        assert created_assistant_profile.id is not None
        assert created_assistant_profile.name == "Assistant"
        assert created_assistant_profile.description == "Store worker"

        # Verifica se o perfil Manager foi persistido no banco
        db_profile = self.db_session.query(ProfileModel).filter_by(name="Manager").first()
        assert db_profile is not None
        assert db_profile.name == "Manager"

        # Verifica se o perfil Assistant foi persistido no banco
        db_profile = self.db_session.query(ProfileModel).filter_by(name="Assistant").first()
        assert db_profile is not None
        assert db_profile.name == "Assistant"
    
    def test_create_duplicate_profile_return_error(self, db_session):
        '''
        Testa erro ao criar um perfil com o nome duplicado
        '''

        # Criando a primeira permissão
        new_profile = Profile(name="Manager", description="Store Manager")
        self.repository.create(new_profile)

        # Tentando criar a permissão duplicada
        duplicate_profile = Profile(name="Manager", description="Store Manager again")
        with pytest.raises(IntegrityError):
            self.repository.create(duplicate_profile)

    def test_get_profile_by_name_success(self):
        '''
        Testa a recuperação de um perfil pelo nome com sucesso
        '''

        # Criando o primeiro perfil
        new_profile = Profile(name="Manager", description="Store Manager")
        created_profile = self.repository.create(new_profile)

        profile = self.repository.get_by_name(created_profile.name)

        assert profile is not None
        assert profile.id == created_profile.id
        assert profile.name == created_profile.name
        assert profile.description == created_profile.description

    def test_get_profile_by_name_with_name_not_registered(self):
        '''
        Testa a busca de um perfil com um nome que não está registrado
        '''

        # Criando o primeiro perfil
        new_profile = Profile(name="Manager", description="Store Manager")
        self.repository.create(new_profile)

        profile = self.repository.get_by_name('not a name')

        assert profile is None
    
    def test_get_profile_by_id_success(self):
        '''
        Testa a recuperação de um perfil pelo id
        '''

        # Criando o primeiro perfil
        new_profile = Profile(name="Manager", description="Store Manager")
        created_profile = self.repository.create(new_profile)

        profile = self.repository.get_by_id(created_profile.id)

        assert profile is not None
        assert profile.id == created_profile.id
        assert profile.name == created_profile.name
        assert profile.description == created_profile.description

    def test_get_profile_by_id_with_id_not_registered(self):
        '''
        Testa a busca de um perfil com um id não registrado
        '''

        # Criando o primeiro perfil
        new_profile = Profile(name="Manager", description="Store Manager")
        self.repository.create(new_profile)

        profile = self.repository.get_by_id(2)

        assert profile is None
    
    def test_get_all_profiles(self):
        '''
        Testa a busca de todos os perfis
        '''

        # Criando os perfiis
        profile1 = Profile(name="Manager", description="Store Manager")
        profile2 = Profile(name="Assistant", description="Store worker")

        self.repository.create(profile1)
        self.repository.create(profile2)

        profiles = self.repository.get_all()

        assert len(profiles) == 2
        assert profiles[0].name == 'Manager'
        assert profiles[1].name == 'Assistant'
    
    def test_get_all_profiles_with_empty_db(self):
        '''
        Testa a busca de todos os perfis com o banco de dados vazio
        '''

        profiles = self.repository.get_all()
        assert len(profiles) == 0
        assert profiles == []
    
    def test_update_profile(self):
        '''
        Testa a atualização de um perfil
        '''

        profile = Profile(name="Manager", description="Store Manager")
        created_profile = self.repository.create(profile)

        created_profile.name = 'Manager - updated'
        created_profile.description = 'Store Manager - updated'

        updated_profile = self.repository.update(created_profile)

        assert updated_profile.name == created_profile.name
        assert updated_profile.description == created_profile.description

    def test_delete_profile(self):
        '''
        Testa a deleção de um perfil
        '''

        profile = Profile(name="Manager", description="Store Manager")
        created_profile = self.repository.create(profile)

        self.repository.delete(created_profile.id)

        assert len(self.repository.get_all()) == 0

    def test_delete_profile_with_inexistent_id(self):
        profile = Profile(name="Manager", description="Store Manager")
        self.repository.create(profile)

        self.repository.delete(2)

        assert len(self.repository.get_all()) == 1

        

from abc import ABC, abstractmethod

from src.core.domain.entities.profile import Profile


class IProfileRepository(ABC):

    @abstractmethod
    def create(profile: Profile):
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Profile:
        pass

    @abstractmethod
    def get_by_id(self, profile_id: int) -> Profile:
        pass
    
    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> Profile:
        pass

    @abstractmethod
    def update(self, profile: Profile) -> Profile:
        pass

    @abstractmethod
    def delete(self, profile_id: int) -> None:
        pass

from datetime import datetime
from typing import Optional
from src.core.domain.entities.base_entity import BaseEntity
import bcrypt

class User(BaseEntity):
    def __init__(
        self,
        name: str,
        password: Optional[str] = None,
        password_hash: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._name = name
        self._password_hash = password_hash
        if password:
            self.password = password

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property 
    def password(self):
        raise AttributeError('Password not readable')
    
    @property
    def password_hash(self):
        return self._password_hash


    @password.setter
    def password(self, password: str) -> None:
        enc_pw = password.encode('utf-8')
        self._password_hash = bcrypt.hashpw(enc_pw, bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self._password_hash.encode('utf-8'))

    @classmethod
    def hash_password(cls, password: str) -> str:
        enc_pw = password.encode('utf-8')
        return bcrypt.hashpw(enc_pw, bcrypt.gensalt()).decode('utf-8')

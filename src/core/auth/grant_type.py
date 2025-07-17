from enum import Enum

class GrantType(str, Enum):
    PASSWORD = "password"
    CPF = "cpf"
    ANONYMOUS = "anonymous"

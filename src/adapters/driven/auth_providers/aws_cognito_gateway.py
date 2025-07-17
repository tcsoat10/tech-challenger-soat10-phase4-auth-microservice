from http import HTTPStatus
from src.core.domain.entities.person import Person
from src.core.ports.auth.i_auth_provider_gateway import IAuthProviderGateway
import os
import requests


class AWSCognitoGateway(IAuthProviderGateway):
    """
    Implementação do gateway de autenticação usando o AWS Cognito.
    """

    def __init__(self):
        self.base_url = os.getenv('APIGW_URL')
        self.headers = { "Content-Type": "application/json" }
    
    def authenticate(self, cpf: str) -> bool:
        """
        Autentica um usuário com o AWS Cognito.
        Retorna True se a autenticação for bem-sucedida, False caso contrário.
        """

        if not cpf:
            print("CPF não fornecido para autenticação.")
            return False

        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"cpf": cpf},
                headers=self.headers
            )
            
            return response.status_code == HTTPStatus.OK
        except Exception as e:
            print(f"Erro ao autenticar usuário: {str(e)}")
            return False

    def sync_user(self, person: Person) -> None:
        """
        Sincroniza os dados do usuário com o AWS Cognito.
        """
        if not person:
            print("Objeto Person não fornecido para sincronização.")
            return
        
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={
                    "cpf": person.cpf,
                    "email": person.email,
                    "name": person.name,
                    "birthdate": person.birth_date.isoformat() if person.birth_date else None
                },
                headers=self.headers
            )
            
            # show response status code and text
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            
            if response.status_code != HTTPStatus.OK:
                print(f"Erro ao sincronizar usuário: {response.text}")
        except Exception as e:
            print(f"Erro ao sincronizar usuário: {str(e)}")

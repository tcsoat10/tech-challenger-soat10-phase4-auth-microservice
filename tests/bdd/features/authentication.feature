Feature: Autenticação de Usuários
  Como um usuário do sistema
  Eu quero me autenticar
  Para acessar as funcionalidades correspondentes ao meu perfil

  Background:
    Given que o sistema está funcionando

  Scenario: Login bem-sucedido de cliente com CPF
    Given existe um perfil "customer" com as permissões:
      | can_create_order |
      | can_view_order   |
      | can_view_products |
    And existe um cliente com CPF "123.456.789-00" cadastrado
    When eu faço login com o CPF "123.456.789-00"
    Then eu devo receber um token de acesso
    And o token deve conter as informações do usuário com CPF "123.456.789-00"
    And o token deve conter o perfil "customer"
    And o token deve conter as permissões:
      | can_create_order |
      | can_view_order   |
      | can_view_products |

  Scenario: Login de cliente com CPF não cadastrado
    Given existe um perfil "customer" cadastrado
    When eu faço login com o CPF "999.999.999-99" que não está cadastrado
    Then eu devo receber um erro de "usuário não encontrado"


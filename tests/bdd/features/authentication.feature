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

  Scenario: Login bem-sucedido de funcionário
    Given existe um perfil "employee" com as permissões:
      | can_list_orders        |
      | can_view_order         |
      | can_update_order_status |
    And existe um funcionário com usuário "jane.doe" e senha "password123"
    When eu faço login com usuário "jane.doe" e senha "password123"
    Then eu devo receber um token de acesso
    And o token deve conter o perfil "employee"
    And o token deve conter as permissões:
      | can_list_orders        |
      | can_view_order         |
      | can_update_order_status |

  Scenario: Login de funcionário com senha incorreta
    Given existe um perfil "employee" com a permissão "can_list_orders"
    And existe um funcionário com usuário "jane.doe" e senha "password123"
    When eu faço login com usuário "jane.doe" e senha "wrong_password"
    Then eu devo receber um erro de "credenciais inválidas"

  Scenario: Login anônimo de cliente
    Given existe um perfil "customer" com as permissões:
      | can_view_products |
      | can_view_order   |
    When eu faço um login anônimo
    Then eu devo receber um token de acesso
    And o token deve conter o perfil "customer"
    And o token deve conter as permissões:
      | can_view_products |
      | can_view_order   |

  Scenario: Login de gerente com permissões específicas
    Given existe um perfil "manager" com as permissões:
      | can_list_orders         |
      | can_view_order          |
      | can_update_order_status |
      | can_view_employees      |
    And existe um gerente com usuário "manager.user" e senha "manager123"
    When eu faço login com usuário "manager.user" e senha "manager123"
    Then eu devo receber um token de acesso
    And o token deve conter o perfil "manager"
    And o token deve conter as permissões:
      | can_list_orders         |
      | can_view_order          |
      | can_update_order_status |
      | can_view_employees      |

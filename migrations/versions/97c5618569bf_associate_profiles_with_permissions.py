"""associate profiles with permissions

Revision ID: 97c5618569bf
Revises: 97b5618569bf
Create Date: 2025-01-11 18:45:12.951580

"""

import os
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import Integer, String, DateTime, MetaData
from datetime import datetime, timezone
from src.constants.permissions import (
    CategoryPermissions,
    CustomerPermissions,
    ProductPermissions,
    OrderItemPermissions,
    OrderPermissions,
    OrderStatusPermissions,
    OrderPaymentPermissions,
    PermissionPermissions,
    ProfilePermissions,
    ProfilePermissionPermissions,
    PaymentMethodPermissions,
    PaymentPermissions,
    PaymentStatusPermissions,
    RolePermissions,
    UserPermissions,
    UserProfilePermissions,
    EmployeePermissions,
    PersonPermissions
)

# Revisão e informações básicas da migração
revision = '97c5618569bf'
down_revision = '97b5618569bf'
branch_labels = None
depends_on = None

# Tabela de referência
profile_permissions_table = table(
    'profile_permissions',
    column('profile_id', String),
    column('permission_id', String),
    column('created_at', DateTime)
)

permissions_table = table(
    'permissions',
    column('id', Integer),
    column('name', String)
)


# Perfis e permissões associadas
profile_permissions = {
    "1": [  # Administrator: todas as permissões
        *CategoryPermissions.values(),
        *ProductPermissions.values(),
        *OrderPermissions.values(),
        *OrderItemPermissions.values(),
        *OrderStatusPermissions.values(),
        *OrderPaymentPermissions.values(),
        *PermissionPermissions.values(),
        *ProfilePermissions.values(),
        *ProfilePermissionPermissions.values(),
        *PaymentMethodPermissions.values(),
        *PaymentPermissions.values(),
        *PaymentStatusPermissions.values(),
        *RolePermissions.values(),
        *UserPermissions.values(),
        *UserProfilePermissions.values(),
        *EmployeePermissions.values(),
        *CustomerPermissions.values(),
        *PersonPermissions.values(),
    ],
    "2": [  # Manager: todas as permissões
        *CategoryPermissions.values(),
        *ProductPermissions.values(),
        *OrderPermissions.list_except_values(except_=['CAN_CREATE', 'CAN_ADD', 'CAN_REMOVE', 'CAN_CHANGE', 'CAN_CLEAR', 'CAN_NEXT', 'CAN_GO']),
        *OrderItemPermissions.values(),
        *OrderStatusPermissions.values(),
        *OrderPaymentPermissions.values(),
        *PermissionPermissions.values(),
        *ProfilePermissions.values(),
        *ProfilePermissionPermissions.values(),
        *PaymentMethodPermissions.values(),
        *PaymentPermissions.values(),
        *PaymentStatusPermissions.values(),
        *RolePermissions.values(),
        *UserPermissions.values(),
        *UserProfilePermissions.values(),
        *EmployeePermissions.values(),
        *CustomerPermissions.values(),
        *PersonPermissions.values(),
    ],
    "3": [  # Employee: acesso limitado
        *CategoryPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
        *ProductPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
        *OrderItemPermissions.values(),
        *OrderPermissions.list_except_values(except_=['CAN_CREATE', 'CAN_ADD', 'CAN_REMOVE', 'CAN_CHANGE', 'CAN_CLEAR', 'CAN_NEXT', 'CAN_GO']),
        *OrderStatusPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
        *OrderPaymentPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
        *PermissionPermissions.list_only_values(only=["CAN_VIEW"]),
        *ProfilePermissions.list_only_values(only=["CAN_VIEW"]),
        *ProfilePermissionPermissions.list_only_values(only=["CAN_VIEW"]),
        *RolePermissions.list_only_values(only=["CAN_VIEW"]),
        *PaymentMethodPermissions.list_only_values(only=["CAN_VIEW"]),
        *PaymentStatusPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
        *UserPermissions.list_only_values(only=["CAN_VIEW"]),
        *UserProfilePermissions.list_only_values(only=["CAN_VIEW"]),
        *EmployeePermissions.list_only_values(only=["CAN_VIEW"]),
        *CustomerPermissions.list_only_values(only=["CAN_VIEW"]),
        *PersonPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
    ],
    "4": [  # Customer: acesso mínimo
        *OrderPermissions.values(),
        *CustomerPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
        *PaymentPermissions.list_only_values(only=["CAN_CREATE", "CAN_VIEW"]),
        *PaymentMethodPermissions.list_only_values(only=["CAN_VIEW"]),
    ]
}

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    permissions_mapping = {}
    result = connection.execute(select(permissions_table.c.id, permissions_table.c.name))
    for row in result:
        permissions_mapping[row[1]] = row[0]

    insert_data = []
    for profile_id, permissions in profile_permissions.items():
        for permission_name in permissions:
            permission_id = permissions_mapping.get(permission_name)
            if permission_id:
                insert_data.append({
                    "profile_id": int(profile_id),
                    "permission_id": permission_id,
                    "created_at": datetime.now(timezone.utc)
                })

    op.bulk_insert(profile_permissions_table, insert_data)


def downgrade():
    op.execute("DELETE FROM profile_permissions WHERE profile_id IN ('1', '2', '3')")
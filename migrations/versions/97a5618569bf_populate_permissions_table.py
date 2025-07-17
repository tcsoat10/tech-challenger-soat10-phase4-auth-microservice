"""populate permissions table

Revision ID: 97a5618569bf
Revises: af6a351d5427
Create Date: 2025-01-11 18:21:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String

from src.constants.permissions import (
    CategoryPermissions,
    CustomerPermissions,
    PersonPermissions,
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
)

# Revisão e informações básicas da migração
revision = '97a5618569bf'
down_revision: Union[str, None] = '91653586a8fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

permissions_table = table(
    'permissions',
    column('id', String),
    column('name', String),
    column('description', String)
)

permissions = [
    # Categories
    *CategoryPermissions.values_and_descriptions(),

    # Products
    *ProductPermissions.values_and_descriptions(),

    # Order Items
    *OrderItemPermissions.values_and_descriptions(),

    # Orders
    *OrderPermissions.values_and_descriptions(),

    # Order Status
    *OrderStatusPermissions.values_and_descriptions(),

    # Order Payment
    *OrderPaymentPermissions.values_and_descriptions(),

    # Permissions
    *PermissionPermissions.values_and_descriptions(),

    # Profile
    *ProfilePermissions.values_and_descriptions(),

    # Profile Permissions
    *ProfilePermissionPermissions.values_and_descriptions(),

    # Payment Methods
    *PaymentMethodPermissions.values_and_descriptions(),

    # Payments
    *PaymentPermissions.values_and_descriptions(),

    # Payment Status
    *PaymentStatusPermissions.values_and_descriptions(),

    # Roles
    *RolePermissions.values_and_descriptions(),

    # Users
    *UserPermissions.values_and_descriptions(),

    # User Profiles
    *UserProfilePermissions.values_and_descriptions(),

    # Employees
    *EmployeePermissions.values_and_descriptions(),

    # Customers
    *CustomerPermissions.values_and_descriptions(),

    # Person
    *PersonPermissions.values_and_descriptions(),
]


def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.bulk_insert(permissions_table, permissions)


def downgrade():
    op.execute("DELETE FROM permissions WHERE name LIKE 'can_%'")

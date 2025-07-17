"""populate profile table

Revision ID: 97b5618569bf
Revises: 97a5618569bf
Create Date: 2025-01-11 18:21:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String

# Revisão e informações básicas da migração
revision = '97b5618569bf'
down_revision: Union[str, None] = '97a5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

profiles_table = table(
    'profiles',
    column('id', String),
    column('name', String),
    column('description', String)
)

profiles = [
    {"name": "administrator", "description": "Manager with full access."},
    {"name": "manager", "description": "Manager with full access."},
    {"name": "employee", "description": "Employee with restricted access."},
    {"name": "customer", "description": "Customer with limited access."},
]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(profiles_table, profiles)

def downgrade():
    op.execute(
        "DELETE FROM profiles WHERE name IN ('manager', 'employee', 'customer')"
    )

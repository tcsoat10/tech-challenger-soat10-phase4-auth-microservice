"""populate user table

Revision ID: 97h5618569bf
Revises: 97g5618569bf
Create Date: 2025-01-19 13:31:12.951580

"""

import os
import bcrypt
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer


# Revisão e informações básicas da migração
revision = '97h5618569bf'
down_revision: Union[str, None] = '97g5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

users_table = table(
    'users',
    column('id', Integer),
    column('name', String),
    column('password_hash', String)
)


users = [
    {
        'name': 'employee',
        'password_hash': bcrypt.hashpw('employee'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    },
    {
        'name': 'manager',
        'password_hash': bcrypt.hashpw('manager'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    }
]
    

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(users_table, users)

def downgrade():
    op.execute(
        "DELETE FROM users WHERE name IN ('employee', 'manager')"
    )

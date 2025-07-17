"""populate person table

Revision ID: 97i5618569bf
Revises: 97h5618569bf
Create Date: 2025-01-19 13:31:12.951580

"""

import os
import bcrypt
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date
from datetime import datetime

# Revisão e informações básicas da migração
revision = '97i5618569bf'
down_revision: Union[str, None] = '97h5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

persons_table = table(
    'persons',
    column('id', Integer),
    column('cpf', String),
    column('name', String),
    column('email', String),
    column('birth_date', Date)
)


persons = [
    {
        'name': 'customer', 
        'cpf': '03619966087',
        'email': 'customer@soat.com',
        'birth_date': datetime.strptime("06/10/2001", "%d/%m/%Y")
    },
    {
        'name': 'employee',
        'cpf': '66087134018',
        'email': 'employee@soat.com',
        'birth_date': datetime.strptime("25/10/2001", "%d/%m/%Y")
    },
    {
        'name': 'manager',
        'cpf': '94352572080',
        'email': 'manager@soat.com',
        'birth_date': datetime.strptime("22/11/1998", "%d/%m/%Y")
    }
]
    

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(persons_table, persons)

def downgrade():
    op.execute(
        "DELETE FROM persons WHERE cpf IN ('03619966087', '66087134018', '94352572080')"
    )

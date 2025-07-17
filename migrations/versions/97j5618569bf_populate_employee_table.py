"""populate employee table

Revision ID: 97j5618569bf
Revises: 97h5618569bf
Create Date: 2025-01-19 13:31:12.951580

"""

import os
import bcrypt
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, Date, MetaData
from datetime import datetime

# Revisão e informações básicas da migração
revision = '97j5618569bf'
down_revision: Union[str, None] = '97h5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

employees_table = table(
    'employees',
    column('id', Integer),
    column('person_id', Integer),
    column('role_id', Integer),
    column('admission_date', Date),
    column('termination_date', Date),
    column('user_id', Integer)
)

persons_table = table(
    'persons',
    column('id', Integer),
    column('name', String)
)

roles_table = table(
    'roles',
    column('id', Integer),
    column('name', String)
)

users_table = table(
    'users',
    column('id', Integer),
    column('name', String)
)


employees = [
    {
        'name': 'employee', 
        'role': 'employee',
        'user': 'employee',
        'admission_date': datetime.strptime("06/12/2024", "%d/%m/%Y")
    },
    {
        'name': 'manager', 
        'role': 'manager',
        'user': 'manager',
        'admission_date': datetime.strptime("06/01/2024", "%d/%m/%Y")
    }
]
    

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    persons_mapping = {}
    result = connection.execute(select(persons_table.c.id, persons_table.c.name))
    for row in result:
        persons_mapping[row[1]] = row[0]
    
    roles_mapping = {}
    result = connection.execute(select(roles_table.c.id, roles_table.c.name))
    for row in result:
        roles_mapping[row[1]] = row[0]

    users_mapping = {}
    result = connection.execute(select(users_table.c.id, users_table.c.name))
    for row in result:
        users_mapping[row[1]] = row[0]

    insert_data = []
    for employee in employees:
        person_id = persons_mapping.get(employee['name'])
        role_id = roles_mapping.get(employee['role'])
        user_id = users_mapping.get(employee['user'])
        if person_id and role_id and user_id:
            insert_data.append({
                'person_id': person_id,
                'role_id': role_id,
                'admission_date': employee['admission_date'],
                'termination_date': None,
                'user_id': user_id

            })
    
    op.bulk_insert(employees_table, insert_data)

def downgrade():
    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    persons_mapping = {}
    result = connection.execute(select(persons_table.c.id, persons_table.c.name))
    for row in result:
        persons_mapping[row[1]] = row[0]
    
    persons_id_list = []
    for employee in employees:
        person_id = persons_mapping.get(employee['name'])
        if person_id:
            persons_id_list.append(person_id)

    op.execute(
        f"DELETE FROM employees WHERE person_id IN ({persons_id_list[0]}, {persons_id_list[1]}, {persons_id_list[2]})"
    )

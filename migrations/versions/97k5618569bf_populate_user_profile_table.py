"""populate user profile table

Revision ID: 97k5618569bf
Revises: 97j5618569bf
Create Date: 2025-01-19 13:31:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, MetaData


# Revisão e informações básicas da migração
revision = '97k5618569bf'
down_revision: Union[str, None] = '97j5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_profiles_table = table(
    'user_profiles',
    column('user_id', Integer),
    column('profile_id', Integer)
)

profiles_table = table(
    'profiles',
    column('id', Integer),
    column('name', String)
)

users_table = table(
    'users',
    column('id', Integer),
    column('name', String)
)


user_profiles = [
    {
        'user': 'employee',
        'profile': 'employee'
    },
    {
        'user': 'manager',
        'profile': 'manager'
    }
]
    

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)
    
    profiles_mapping = {}
    result = connection.execute(select(profiles_table.c.id, profiles_table.c.name))
    for row in result:
        profiles_mapping[row[1]] = row[0]

    users_mapping = {}
    result = connection.execute(select(users_table.c.id, users_table.c.name))
    for row in result:
        users_mapping[row[1]] = row[0]

    insert_data = []
    for user_profile in user_profiles:
        profile_id = profiles_mapping.get(user_profile['profile'])
        user_id = users_mapping.get(user_profile['user'])
        if profile_id and user_id:
            insert_data.append({
                'profile_id': profile_id,
                'user_id': user_id
            })
    
    op.bulk_insert(user_profiles_table, insert_data)

def downgrade():
    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    users_mapping = {}
    result = connection.execute(select(users_table.c.id, users_table.c.name))
    for row in result:
        users_mapping[row[1]] = row[0]
    
    users_id_list = []
    for user_profile in user_profiles:
        user_id = users_mapping.get(user_profile['user'])
        if user_id:
            users_id_list.append(user_id)

    op.execute(
        f"DELETE FROM user_profiles WHERE user_id IN ({users_id_list[0]}, {users_id_list[1]}, {users_id_list[2]})"
    )

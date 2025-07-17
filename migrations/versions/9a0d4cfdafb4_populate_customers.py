"""Populate customers

Revision ID: 9a0d4cfdafb4
Revises: 97i5618569bf
Create Date: 2025-01-21 21:44:11.725559

"""
import os
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '9a0d4cfdafb4'
down_revision: Union[str, None] = '97i5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


customers = [
    {'id': 1, 'person_id': 1},
]

def upgrade() -> None:
    if os.getenv("ENVIRONMENT") == "testing":
        return

    for customer in customers:
        op.execute(
            f"""
            INSERT INTO customers (id, person_id)
            VALUES ({customer['id']}, {customer['person_id']})
            """
        )

def downgrade() -> None:
    if os.getenv("ENVIRONMENT") == "testing":
        return

    for customer in reversed(customers):
        op.execute(
            f"""
            DELETE FROM customers
            WHERE id = {customer['id']}
            """
        )

"""empty message

Revision ID: 79146ba9f218
Revises: 97k5618569bf, 9a0d4cfdafb4
Create Date: 2025-07-16 01:38:36.440232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79146ba9f218'
down_revision: Union[str, None] = ('97k5618569bf', '9a0d4cfdafb4')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

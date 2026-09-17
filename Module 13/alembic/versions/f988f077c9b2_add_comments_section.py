"""add comments section

Revision ID: f988f077c9b2
Revises: eaf1312538a3
Create Date: 2026-09-14 00:36:27.494040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f988f077c9b2'
down_revision: Union[str, Sequence[str], None] = 'eaf1312538a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('comments', sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'comments')

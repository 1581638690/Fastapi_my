"""create posts table

Revision ID: 0dc2772effe5
Revises: 
Create Date: 2024-01-15 14:54:11.642590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dc2772effe5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                                       primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    pass

"""add_content_column_to_posts

Revision ID: 10e129ad85a5
Revises: 6c4536699ec0
Create Date: 2024-01-15 14:59:08.084371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10e129ad85a5'
down_revision: Union[str, None] = '6c4536699ec0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

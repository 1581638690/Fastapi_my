"""add_last_few_columns_to_posts_table

Revision ID: 8d51f3a51c58
Revises: 3537cef2b821
Create Date: 2024-01-15 15:00:52.539316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8d51f3a51c58'
down_revision: Union[str, None] = '3537cef2b821'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'), )
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')), )
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

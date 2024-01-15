"""add foreign_key_to_posts_table

Revision ID: 3537cef2b821
Revises: 10e129ad85a5
Create Date: 2024-01-15 15:00:19.572602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3537cef2b821'
down_revision: Union[str, None] = '10e129ad85a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass

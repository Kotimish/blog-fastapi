"""create users table

Revision ID: 2d3f9295282c
Revises: 
Create Date: 2025-10-17 00:23:19.227996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2d3f9295282c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'username',
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            'email',
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            'full_name',
            sa.String(length=100),
            server_default='',
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_users'),
        ),
        sa.UniqueConstraint(
            'email',
            name=op.f('uq_users_email'),
        ),
        sa.UniqueConstraint(
            'username',
            name=op.f('uq_users_username'),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')

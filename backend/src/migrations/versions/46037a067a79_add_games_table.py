"""add games table

Revision ID: 46037a067a79
Revises: d8592db52794
Create Date: 2025-12-06 12:45:25.642096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from uuid import uuid4


# revision identifiers, used by Alembic.
revision: str = '46037a067a79'
down_revision: Union[str, Sequence[str], None] = 'd8592db52794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'games',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('energy_cost', sa.Integer(), nullable=False, server_default="1"),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    games_table = sa.table(
        "games",
        sa.column("id", sa.Uuid()),
        sa.column("slug", sa.String()),
        sa.column("name", sa.String()),
        sa.column("energy_cost", sa.Integer()),
    )
    defaults = [
        {"slug": "flappy", "name": "Flappy Gift", "energy_cost": 1},
        {"slug": "osu", "name": "Osu Lite", "energy_cost": 1},
        {"slug": "ski", "name": "Ski Run", "energy_cost": 1},
        {"slug": "lumberjack", "name": "Ice Lumberjack", "energy_cost": 1},
    ]
    op.bulk_insert(
        games_table,
        [{"id": uuid4(), **row} for row in defaults],
    )

    op.alter_column(
        'game_sessions',
        'game_id',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.create_foreign_key(
        'fk_game_sessions_game_id',
        'game_sessions',
        'games',
        ['game_id'],
        ['slug'],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_game_sessions_game_id', 'game_sessions', type_='foreignkey')
    op.alter_column('game_sessions', 'game_id',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    op.drop_table('games')

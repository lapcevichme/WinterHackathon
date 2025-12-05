"""transfer user columns

Revision ID: fa987870e5e1
Revises: a629654c84b7
Create Date: 2025-12-05 21:41:29.436221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa987870e5e1'
down_revision: Union[str, Sequence[str], None] = 'a629654c84b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_cols = {col["name"] for col in inspector.get_columns("users")}

    def _add_if_missing(name: str, column: sa.Column) -> None:
        if name not in existing_cols:
            op.add_column("users", column)

    _add_if_missing("display_name", sa.Column("display_name", sa.String(length=50), nullable=True))
    _add_if_missing("max_score", sa.Column("max_score", sa.Integer(), nullable=False, server_default="0"))
    _add_if_missing("score", sa.Column("score", sa.Integer(), nullable=False, server_default="0"))
    _add_if_missing("level", sa.Column("level", sa.Integer(), nullable=False, server_default="0"))
    _add_if_missing("amount", sa.Column("amount", sa.Integer(), nullable=False, server_default="0"))
    _add_if_missing("energy", sa.Column("energy", sa.Integer(), nullable=False, server_default="10"))
    _add_if_missing("role", sa.Column("role", sa.String(length=20), nullable=False, server_default="player"))

    # Create unique constraint for username if not exists
    constraints = {c["name"] for c in inspector.get_unique_constraints("users")}
    if "users_username_key" not in constraints:
        op.create_unique_constraint('users_username_key', 'users', ['username'])

    # Drop obsolete columns if they exist
    for col_name in ("birth_date", "is_onboarded", "bio"):
        if col_name in existing_cols:
            op.drop_column("users", col_name)


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_cols = {col["name"] for col in inspector.get_columns("users")}

    if 'users_username_key' in {c["name"] for c in inspector.get_unique_constraints("users")}:
        op.drop_constraint('users_username_key', 'users', type_='unique')

    for col_name in ("role", "energy", "amount", "level", "score", "max_score", "display_name"):
        if col_name in existing_cols:
            op.drop_column('users', col_name)

    # Restore dropped columns for full downgrade
    for name, column in [
        ("bio", sa.Column('bio', sa.VARCHAR(), autoincrement=False, nullable=True)),
        ("is_onboarded", sa.Column('is_onboarded', sa.BOOLEAN(), autoincrement=False, nullable=False, server_default=sa.text("false"))),
        ("birth_date", sa.Column('birth_date', sa.DATE(), autoincrement=False, nullable=True)),
    ]:
        if name not in existing_cols:
            op.add_column('users', column)

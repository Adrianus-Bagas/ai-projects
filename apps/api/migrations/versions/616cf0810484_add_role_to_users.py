"""add role to users

Revision ID: 616cf0810484
Revises: 522aa84d25d5
Create Date: 2026-07-26 05:59:30.702352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '616cf0810484'
down_revision: Union[str, Sequence[str], None] = '522aa84d25d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add role column to users."""

    user_role = postgresql.ENUM(
        "user",
        "admin",
        name="user_role",
        create_type=False,
    )

    user_role.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="user",
        ),
    )

    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Remove role column from users."""

    op.drop_column(
        "users",
        "role",
    )

    user_role = postgresql.ENUM(
        "user",
        "admin",
        name="user_role",
        create_type=False,
    )

    user_role.drop(
        op.get_bind(),
        checkfirst=True,
    )

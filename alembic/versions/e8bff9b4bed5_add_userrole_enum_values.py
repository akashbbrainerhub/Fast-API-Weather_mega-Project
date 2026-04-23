"""add userrole enum values

Revision ID: e8bff9b4bed5
Revises: 016c2641b2e2
Create Date: 2026-04-23 13:16:20.219190

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e8bff9b4bed5'
down_revision: Union[str, Sequence[str], None] = '016c2641b2e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # PostgreSQL enum values are append-only; add labels idempotently.
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE t.typname = 'userrole' AND e.enumlabel = 'ANALYST'
            ) THEN
                ALTER TYPE userrole ADD VALUE 'ANALYST';
            END IF;

            IF NOT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE t.typname = 'userrole' AND e.enumlabel = 'MODERATOR'
            ) THEN
                ALTER TYPE userrole ADD VALUE 'MODERATOR';
            END IF;

            IF NOT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE t.typname = 'userrole' AND e.enumlabel = 'PREMIUM_USER'
            ) THEN
                ALTER TYPE userrole ADD VALUE 'PREMIUM_USER';
            END IF;
        END
        $$;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Removing enum labels is not safely reversible in PostgreSQL.
    pass

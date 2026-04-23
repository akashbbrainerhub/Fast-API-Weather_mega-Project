"""restore missing revision anchor

Revision ID: 016c2641b2e2
Revises: 663a96a790c2
Create Date: 2026-04-23 12:00:00.000000

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "016c2641b2e2"
down_revision: Union[str, Sequence[str], None] = "663a96a790c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""update weather fields

Revision ID: 663a96a790c2
Revises: ad3df941ec63
Create Date: 2026-04-22 17:25:00.686636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '663a96a790c2'
down_revision: Union[str, Sequence[str], None] = 'ad3df941ec63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('weather', sa.Column('pressure', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('wind_speed', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('description', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('weather', 'description')
    op.drop_column('weather', 'wind_speed')
    op.drop_column('weather', 'pressure')

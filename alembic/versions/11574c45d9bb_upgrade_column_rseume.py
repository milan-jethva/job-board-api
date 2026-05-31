"""upgrade column rseume

Revision ID: 11574c45d9bb
Revises: a004b568a11f
Create Date: 2026-05-30 16:13:15.354098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11574c45d9bb'
down_revision: Union[str, Sequence[str], None] = 'a004b568a11f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

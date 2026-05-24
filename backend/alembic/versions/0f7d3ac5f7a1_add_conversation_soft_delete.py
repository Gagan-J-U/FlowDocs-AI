"""add conversation soft delete

Revision ID: 0f7d3ac5f7a1
Revises: 5caa8c790db3
Create Date: 2026-05-24 00:00:00.000000
"""

from typing import Sequence
from typing import Union

from alembic import op


revision: str = "0f7d3ac5f7a1"
down_revision: Union[str, None] = "5caa8c790db3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE conversations "
        "ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITHOUT TIME ZONE"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE conversations "
        "DROP COLUMN IF EXISTS deleted_at"
    )

"""add is_sections_approved to legalcase

Revision ID: 935fee312e88
Revises: 7ae0cc35cfdb
Create Date: 2026-06-07 15:47:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '935fee312e88'
down_revision = '7ae0cc35cfdb'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Ye wahi fix hai jo humne pehle kiya tha
    op.add_column('legalcase', sa.Column('is_sections_approved', sa.Boolean(), nullable=False, server_default='false'))

def downgrade() -> None:
    op.drop_column('legalcase', 'is_sections_approved')
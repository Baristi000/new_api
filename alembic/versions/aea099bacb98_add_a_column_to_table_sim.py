"""Add a column to table sim

Revision ID: aea099bacb98
Revises: a8fe7bbcd5d4
Create Date: 2020-09-11 15:17:20.875631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aea099bacb98'
down_revision = 'a8fe7bbcd5d4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('shop', sa.Column('shop_master_id', sa.String(45)))


def downgrade():
    op.drop_column('shop', 'shop_master_id')

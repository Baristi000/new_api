"""add an column

Revision ID: e21418152ed0
Revises: 4261e37546d8
Create Date: 2020-08-31 09:08:22.254181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e21418152ed0'
down_revision = '4261e37546d8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')

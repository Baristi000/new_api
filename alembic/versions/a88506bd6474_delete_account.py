"""delete account

Revision ID: a88506bd6474
Revises: e21418152ed0
Create Date: 2020-08-31 09:12:17.365857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a88506bd6474'
down_revision = 'e21418152ed0'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_table('account')

def downgrade():
    op.drop_table('account')

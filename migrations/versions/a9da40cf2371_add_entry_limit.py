"""add_entry_limit

Revision ID: a9da40cf2371
Revises: db8ced4ce2b2
Create Date: 2019-07-01 23:57:32.993035

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a9da40cf2371'
down_revision = 'db8ced4ce2b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('entry_limit', sa.Integer(), server_default='80', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account', 'entry_limit')
    # ### end Alembic commands ###

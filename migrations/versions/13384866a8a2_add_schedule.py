"""add schedule

Revision ID: 13384866a8a2
Revises: cf04f2a23d02
Create Date: 2019-09-08 21:17:47.324158

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '13384866a8a2'
down_revision = 'cf04f2a23d02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('friday', sa.Integer(), server_default='0', nullable=False))
    op.add_column('user_account', sa.Column('monday', sa.Integer(), server_default='0', nullable=False))
    op.add_column('user_account', sa.Column('saturday', sa.Integer(), server_default='0', nullable=False))
    op.add_column('user_account', sa.Column('sunday', sa.Integer(), server_default='0', nullable=False))
    op.add_column('user_account', sa.Column('thursday', sa.Integer(), server_default='0', nullable=False))
    op.add_column('user_account', sa.Column('tuesday', sa.Integer(), server_default='0', nullable=False))
    op.add_column('user_account', sa.Column('wednesday', sa.Integer(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account', 'wednesday')
    op.drop_column('user_account', 'tuesday')
    op.drop_column('user_account', 'thursday')
    op.drop_column('user_account', 'sunday')
    op.drop_column('user_account', 'saturday')
    op.drop_column('user_account', 'monday')
    op.drop_column('user_account', 'friday')
    # ### end Alembic commands ###

"""add entry history

Revision ID: e354a89547c4
Revises: 85a27b4f273d
Create Date: 2021-01-30 23:06:01.790266

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e354a89547c4"
down_revision = "85a27b4f273d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_account",
        sa.Column("entry_history", sa.Integer(), server_default="12", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_account", "entry_history")
    # ### end Alembic commands ###

"""empty message

Revision ID: f8064550049a
Revises: 72b4953ac3d4
Create Date: 2023-03-05 17:47:34.292681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8064550049a'
down_revision = '72b4953ac3d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account_table', sa.Column('is_admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account_table', 'is_admin')
    # ### end Alembic commands ###

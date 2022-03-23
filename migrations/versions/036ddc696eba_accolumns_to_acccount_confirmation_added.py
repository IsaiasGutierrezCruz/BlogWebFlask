"""AcColumns to acccount confirmation added

Revision ID: 036ddc696eba
Revises: 22ffb930bb1f
Create Date: 2022-03-21 20:00:35.204814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036ddc696eba'
down_revision = '22ffb930bb1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###

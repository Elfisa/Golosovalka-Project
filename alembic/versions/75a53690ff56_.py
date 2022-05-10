"""empty message

Revision ID: 75a53690ff56
Revises: 2517e6aecb13
Create Date: 2022-05-06 04:24:47.772239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75a53690ff56'
down_revision = '2517e6aecb13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('is_published', sa.Boolean(), nullable=True))
    op.add_column('votes', sa.Column('is_hidden', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('votes', 'is_hidden')
    op.drop_column('votes', 'is_published')
    # ### end Alembic commands ###

"""empty message

Revision ID: f4472992a3ec
Revises: 19467925a5a4
Create Date: 2022-05-06 07:16:27.454525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4472992a3ec'
down_revision = '19467925a5a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('icon', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'icon')
    # ### end Alembic commands ###

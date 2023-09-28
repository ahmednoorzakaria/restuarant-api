"""empty message

Revision ID: 524b50f3c162
Revises: 55935bf7bbbc
Create Date: 2023-09-27 14:23:21.660991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '524b50f3c162'
down_revision = '55935bf7bbbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), nullable=True))

    # ### end Alembic commands ###

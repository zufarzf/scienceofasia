"""empty message

Revision ID: 26bf175614af
Revises: eac53ef86530
Create Date: 2023-09-28 02:19:25.641199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26bf175614af'
down_revision = 'eac53ef86530'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('editorial_board_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text', sa.Text(), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('editorial_board_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.TEXT(), nullable=True))
        batch_op.drop_column('text')

    # ### end Alembic commands ###

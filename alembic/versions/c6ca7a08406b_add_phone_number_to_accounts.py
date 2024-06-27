"""Add phone_number to accounts

Revision ID: c6ca7a08406b
Revises: a8854f6dcded
Create Date: 2024-06-27 16:58:25.292532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6ca7a08406b'
down_revision: Union[str, None] = 'a8854f6dcded'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('phone_number', sa.String(), nullable=False))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'phone_number')
    # ### end Alembic commands ###
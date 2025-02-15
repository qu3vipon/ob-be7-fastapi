"""add username unique index

Revision ID: 016a7c04f7c0
Revises: 7e2034ba2657
Create Date: 2025-01-13 11:44:28.493121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '016a7c04f7c0'
down_revision: Union[str, None] = '7e2034ba2657'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uix_service_user_username', 'service_user', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uix_service_user_username', 'service_user', type_='unique')
    # ### end Alembic commands ###

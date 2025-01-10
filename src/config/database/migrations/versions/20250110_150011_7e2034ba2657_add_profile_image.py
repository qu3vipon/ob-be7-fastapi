"""add profile_image

Revision ID: 7e2034ba2657
Revises: 2dc815644d4e
Create Date: 2025-01-10 15:00:11.190624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e2034ba2657'
down_revision: Union[str, None] = '2dc815644d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_user', sa.Column('profile_image', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service_user', 'profile_image')
    # ### end Alembic commands ###

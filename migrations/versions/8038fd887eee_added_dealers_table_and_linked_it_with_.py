"""Added dealers table and linked it with users

Revision ID: 8038fd887eee
Revises: b57ffe529a87
Create Date: 2023-12-18 20:17:03.023169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8038fd887eee'
down_revision: Union[str, None] = 'b57ffe529a87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dealers',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=512), nullable=False),
    sa.Column('address', sa.VARCHAR(length=512), nullable=False),
    sa.Column('contact_phone', sa.VARCHAR(length=11), nullable=False),
    sa.Column('email', sa.VARCHAR(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_dealers')),
    sa.UniqueConstraint('name', 'address', name=op.f('uq_dealers_name'))
    )
    op.create_table('dealer_users',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('dealer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dealer_id'], ['dealers.id'], name=op.f('fk_dealer_users_dealer_id_dealers'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_dealer_users_user_id_users'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'dealer_id', name=op.f('pk_dealer_users'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dealer_users')
    op.drop_table('dealers')
    # ### end Alembic commands ###
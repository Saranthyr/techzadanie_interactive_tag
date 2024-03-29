"""Refactored database structure from scratch

Revision ID: 7e589cd31821
Revises: 
Create Date: 2024-01-31 06:53:27.676912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e589cd31821'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('colours',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_colours'))
    )
    op.create_table('dealers',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_dealers')),
    sa.UniqueConstraint('name', name=op.f('uq_dealers_name'))
    )
    op.create_table('engines',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_engines'))
    )
    op.create_table('kits',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_kits'))
    )
    op.create_table('models',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_models')),
    sa.UniqueConstraint('name', name=op.f('uq_models_name'))
    )
    op.create_table('parameters',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_parameters'))
    )
    op.create_table('transmissions',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_transmissions'))
    )
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.VARCHAR(length=256), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('first_name', 'last_name', name=op.f('uq_users_first_name')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_table('dealer_users',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('dealer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dealer_id'], ['dealers.id'], name=op.f('fk_dealer_users_dealer_id_dealers'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_dealer_users_user_id_users'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'dealer_id', name=op.f('pk_dealer_users'))
    )
    op.create_table('model_kits',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, increment=1), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=False),
    sa.Column('kit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['kit_id'], ['kits.id'], name=op.f('fk_model_kits_kit_id_kits'), onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], name=op.f('fk_model_kits_model_id_models'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_model_kits')),
    sa.UniqueConstraint('model_id', 'kit_id', name=op.f('uq_model_kits_model_id'))
    )
    op.create_table('cars',
    sa.Column('vin', sa.VARCHAR(length=17), nullable=False),
    sa.Column('model_kit', sa.Integer(), nullable=False),
    sa.Column('engine', sa.Integer(), nullable=False),
    sa.Column('transmission', sa.Integer(), nullable=False),
    sa.Column('colour', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['colour'], ['colours.id'], name=op.f('fk_cars_colour_colours'), onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['engine'], ['engines.id'], name=op.f('fk_cars_engine_engines'), onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['model_kit'], ['model_kits.id'], name=op.f('fk_cars_model_kit_model_kits'), onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['transmission'], ['transmissions.id'], name=op.f('fk_cars_transmission_transmissions'), onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('vin', name=op.f('pk_cars'))
    )
    op.create_table('model_kit_parameters',
    sa.Column('model_kit_id', sa.Integer(), nullable=False),
    sa.Column('parameter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['model_kit_id'], ['model_kits.id'], name=op.f('fk_model_kit_parameters_model_kit_id_model_kits'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parameter_id'], ['parameters.id'], name=op.f('fk_model_kit_parameters_parameter_id_parameters'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('model_kit_id', 'parameter_id', name=op.f('pk_model_kit_parameters'))
    )
    op.create_table('dealer_cars',
    sa.Column('dealer_id', sa.Integer(), nullable=False),
    sa.Column('car_vin', sa.VARCHAR(length=17), nullable=False),
    sa.ForeignKeyConstraint(['car_vin'], ['cars.vin'], name=op.f('fk_dealer_cars_car_vin_cars'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['dealer_id'], ['dealers.id'], name=op.f('fk_dealer_cars_dealer_id_dealers'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('dealer_id', 'car_vin', name=op.f('pk_dealer_cars'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dealer_cars')
    op.drop_table('model_kit_parameters')
    op.drop_table('cars')
    op.drop_table('model_kits')
    op.drop_table('dealer_users')
    op.drop_table('users')
    op.drop_table('transmissions')
    op.drop_table('parameters')
    op.drop_table('models')
    op.drop_table('kits')
    op.drop_table('engines')
    op.drop_table('dealers')
    op.drop_table('colours')
    # ### end Alembic commands ###

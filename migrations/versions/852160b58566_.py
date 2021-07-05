"""empty message

Revision ID: 852160b58566
Revises: 6502fd45781f
Create Date: 2021-07-05 11:21:01.869885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '852160b58566'
down_revision = '6502fd45781f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sd00_blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False, comment='JWT refresh token'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Create time'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('sd10_customers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False, comment='Name'),
    sa.Column('display_name', sa.String(length=50), nullable=False, comment='Display name'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('status', sa.Integer(), server_default='0', nullable=False, comment='Status'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Vendor of customer'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sd10_customers_name'), 'sd10_customers', ['name'], unique=True)
    op.create_table('sd18_roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False, comment='authorization role, ex: admin, user'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Display name'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sd30_device_models',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True, comment='Traffic Light part no'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Part description + specification'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sd11_users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False, comment='Name'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Display name'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('status', sa.Integer(), server_default='0', nullable=True, comment='Status'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('password', sa.String(length=64), nullable=True, comment='Password'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.Column('email', sa.String(length=100), nullable=True, comment='Email'),
    sa.Column('telephone', sa.String(length=30), nullable=True, comment='Telephone number'),
    sa.Column('line_id', sa.String(length=30), nullable=True, comment='LINE id'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cust_id', 'name')
    )
    op.create_table('sd12_codes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cust_id', sa.Integer(), nullable=False, comment='Customer id'),
    sa.Column('code_type', sa.Integer(), nullable=True, comment='Code type, specification write in constant'),
    sa.Column('code_no', sa.Integer(), nullable=False, comment='Code number'),
    sa.Column('name', sa.String(length=20), nullable=False, comment='Code name'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Code display name'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sd13_user_groups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False, comment='Name'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Display name'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cust_id', 'name')
    )
    op.create_table('sd17_privileges',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False, comment='authorization role, ex: admin, user'),
    sa.Column('api_route', sa.Text(), nullable=False, comment='API route, each api is unique'),
    sa.ForeignKeyConstraint(['role_id'], ['sd18_roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sd19_status_privileges',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False, comment='authorization role, ex: admin, user'),
    sa.Column('status_from', sa.Integer(), nullable=True, comment='Current state'),
    sa.Column('status_to', sa.Integer(), nullable=True, comment='Next state'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['sd18_roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sd31_controllers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True, comment='Name'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Display name'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.Column('status', sa.Integer(), server_default='0', nullable=True, comment='Device status flag. bit 0: warning, bit 1: error'),
    sa.Column('model_id', sa.Integer(), server_default='0', nullable=True, comment='Traffic Light model/part no'),
    sa.Column('serial_no', sa.String(length=50), nullable=False, comment='Serial No'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['sd30_device_models.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cust_id', 'name'),
    sa.UniqueConstraint('serial_no')
    )
    op.create_table('sd32_leds',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True, comment='Name'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Display name'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.Column('status', sa.Integer(), server_default='0', nullable=True, comment='Device status flag. bit 0: warning, bit 1: error'),
    sa.Column('model_id', sa.Integer(), server_default='0', nullable=True, comment='Traffic Light model/part no'),
    sa.Column('serial_no', sa.String(length=50), nullable=False, comment='Serial No'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['sd30_device_models.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cust_id', 'name'),
    sa.UniqueConstraint('serial_no')
    )
    op.create_table('sd42_schedule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('counting_time', sa.Integer(), nullable=True, comment='紅綠燈從紅燈變為綠燈的等待時間，單位為秒'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sd14_rel_u_ug',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_group_id'], ['sd13_user_groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['sd11_users.id'], )
    )
    op.create_table('sd16_rel_role_ug',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('user_group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['sd18_roles.id'], ),
    sa.ForeignKeyConstraint(['user_group_id'], ['sd13_user_groups.id'], )
    )
    op.create_table('sd22_device_groups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False, comment='Name'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Display name'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.Column('schedule_id', sa.Integer(), nullable=True, comment='Schedule id, null means no schedule'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.ForeignKeyConstraint(['schedule_id'], ['sd42_schedule.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cust_id', 'name')
    )
    op.create_table('sd15_rel_dg_ug',
    sa.Column('device_group_id', sa.Integer(), nullable=True),
    sa.Column('user_group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_group_id'], ['sd22_device_groups.id'], ),
    sa.ForeignKeyConstraint(['user_group_id'], ['sd13_user_groups.id'], )
    )
    op.create_table('sd21_devices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True, comment='Name'),
    sa.Column('display_name', sa.String(length=50), nullable=True, comment='Display name'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('dev_type', sa.Integer(), server_default='0', nullable=True, comment='Device type: 0: unknown, 1: traffic light, 2: others'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.Column('vendor_id', sa.Integer(), nullable=True, comment='Vendor id'),
    sa.Column('status', sa.Integer(), server_default='0', nullable=True, comment='Device status flag(bit).  0: warning, bit 1: error，可持續新增'),
    sa.Column('power_status', sa.Integer(), nullable=True, comment='Device power status. null: unknown, 0: off, 1: on'),
    sa.Column('device_group_id', sa.Integer(), nullable=True, comment='Device group id, null means ungroup'),
    sa.Column('controller_id', sa.Integer(), nullable=True, comment='Controller id'),
    sa.Column('led_id', sa.Integer(), nullable=True, comment='LED id'),
    sa.Column('vender_device_id', sa.String(length=25), nullable=True, comment='Vender device id'),
    sa.Column('wgs_x', sa.Float(), nullable=True, comment='GPS X'),
    sa.Column('wgs_y', sa.Float(), nullable=True, comment='GPS Y'),
    sa.Column('address', sa.String(length=100), nullable=True, comment='Address'),
    sa.ForeignKeyConstraint(['controller_id'], ['sd31_controllers.id'], ),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.ForeignKeyConstraint(['device_group_id'], ['sd22_device_groups.id'], ),
    sa.ForeignKeyConstraint(['led_id'], ['sd32_leds.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['sd10_customers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cust_id', 'name')
    )
    op.create_table('sd23_device_infos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=True, comment='Device id'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Comment'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.Column('voltage', sa.Float(), nullable=True, comment='Voltage'),
    sa.Column('current', sa.Float(), nullable=True, comment='Current'),
    sa.Column('pf', sa.Float(), nullable=True, comment='Power factor'),
    sa.Column('power', sa.Float(), nullable=True, comment='Power value'),
    sa.Column('temperature', sa.Float(), nullable=True, comment='Temperature'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.ForeignKeyConstraint(['device_id'], ['sd21_devices.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cust_id', 'device_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sd23_device_infos')
    op.drop_table('sd21_devices')
    op.drop_table('sd15_rel_dg_ug')
    op.drop_table('sd22_device_groups')
    op.drop_table('sd16_rel_role_ug')
    op.drop_table('sd14_rel_u_ug')
    op.drop_table('sd42_schedule')
    op.drop_table('sd32_leds')
    op.drop_table('sd31_controllers')
    op.drop_table('sd19_status_privileges')
    op.drop_table('sd17_privileges')
    op.drop_table('sd13_user_groups')
    op.drop_table('sd12_codes')
    op.drop_table('sd11_users')
    op.drop_table('sd30_device_models')
    op.drop_table('sd18_roles')
    op.drop_index(op.f('ix_sd10_customers_name'), table_name='sd10_customers')
    op.drop_table('sd10_customers')
    op.drop_table('sd00_blacklist_tokens')
    # ### end Alembic commands ###
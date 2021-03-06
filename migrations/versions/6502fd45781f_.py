"""empty message

Revision ID: 6502fd45781f
Revises: d36d36d39231
Create Date: 2021-06-28 15:46:11.312152

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6502fd45781f'
down_revision = 'd36d36d39231'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sd42_schedule',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('counting_time', sa.Integer(), nullable=True, comment='紅綠燈從紅燈變為綠燈的等待時間，單位為秒'),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Create time'),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Update time'),
    sa.Column('cust_id', sa.Integer(), nullable=True, comment='Customer id'),
    sa.ForeignKeyConstraint(['cust_id'], ['sd10_customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('sd10_customers', 'issue_namespace')
    op.alter_column('sd21_devices', 'dev_type',
               existing_type=sa.INTEGER(),
               comment='Device type: 0: unknown, 1: traffic light, 2: others',
               existing_comment='Device type: 0: unknown, 1: traffic light, 2: large scale devices',
               existing_nullable=True,
               existing_server_default=sa.text('0'))
    op.alter_column('sd21_devices', 'status',
               existing_type=sa.INTEGER(),
               comment='Device status flag(bit).  0: warning, bit 1: error，可持續新增',
               existing_comment='Device status flag. bit 0: warning, bit 1: error',
               existing_nullable=True,
               existing_server_default=sa.text('0'))
    op.drop_column('sd21_devices', 'dimming')
    op.add_column('sd22_device_groups', sa.Column('schedule_id', sa.Integer(), nullable=True, comment='Schedule id, null means no schedule'))
    op.create_foreign_key(None, 'sd22_device_groups', 'sd42_schedule', ['schedule_id'], ['id'])
    op.drop_column('sd23_device_infos', 'lumming')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sd23_device_infos', sa.Column('lumming', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True, comment='Lumming'))
    op.drop_constraint(None, 'sd22_device_groups', type_='foreignkey')
    op.drop_column('sd22_device_groups', 'schedule_id')
    op.add_column('sd21_devices', sa.Column('dimming', sa.INTEGER(), autoincrement=False, nullable=True, comment='Device dimming. 0~100'))
    op.alter_column('sd21_devices', 'status',
               existing_type=sa.INTEGER(),
               comment='Device status flag. bit 0: warning, bit 1: error',
               existing_comment='Device status flag(bit).  0: warning, bit 1: error，可持續新增',
               existing_nullable=True,
               existing_server_default=sa.text('0'))
    op.alter_column('sd21_devices', 'dev_type',
               existing_type=sa.INTEGER(),
               comment='Device type: 0: unknown, 1: traffic light, 2: large scale devices',
               existing_comment='Device type: 0: unknown, 1: traffic light, 2: others',
               existing_nullable=True,
               existing_server_default=sa.text('0'))
    op.add_column('sd10_customers', sa.Column('issue_namespace', sa.VARCHAR(length=50), server_default=sa.text("'CUSTOM-{datetime:%%Y%%m%%d}-{serial_no:05d}'::character varying"), autoincrement=False, nullable=False, comment='Issue number namespace'))
    op.drop_table('sd42_schedule')
    # ### end Alembic commands ###

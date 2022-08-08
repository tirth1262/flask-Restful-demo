"""empty message

Revision ID: 1f5c0971b0ab
Revises: 
Create Date: 2022-08-04 16:50:04.070844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f5c0971b0ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_department_id'), 'department', ['id'], unique=False)
    op.create_table('holidays',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_holidays_date'), 'holidays', ['date'], unique=False)
    op.create_index(op.f('ix_holidays_id'), 'holidays', ['id'], unique=False)
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('firstname', sa.String(length=50), nullable=True),
    sa.Column('lastname', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_role_id'), 'user_role', ['id'], unique=False)
    op.create_table('department_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('user_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_role_id'], ['user_role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_department_user_id'), 'department_user', ['id'], unique=False)
    op.create_table('leave',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('dept_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dept_user_id'], ['department_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leave_end_date'), 'leave', ['end_date'], unique=False)
    op.create_index(op.f('ix_leave_id'), 'leave', ['id'], unique=False)
    op.create_index(op.f('ix_leave_start_date'), 'leave', ['start_date'], unique=False)
    op.create_table('user_head',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dept_user_id', sa.Integer(), nullable=False),
    sa.Column('head_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dept_user_id'], ['department_user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['head_id'], ['department_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_head_id'), 'user_head', ['id'], unique=False)
    op.create_table('leave_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('leave_id', sa.Integer(), nullable=False),
    sa.Column('commenter_id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('time_stamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['commenter_id'], ['department_user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['leave_id'], ['leave.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leave_comments_id'), 'leave_comments', ['id'], unique=False)
    op.create_table('leave_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('leave_id', sa.Integer(), nullable=False),
    sa.Column('approval_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('time_stamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['approval_id'], ['department_user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['leave_id'], ['leave.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leave_status_id'), 'leave_status', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leave_status_id'), table_name='leave_status')
    op.drop_table('leave_status')
    op.drop_index(op.f('ix_leave_comments_id'), table_name='leave_comments')
    op.drop_table('leave_comments')
    op.drop_index(op.f('ix_user_head_id'), table_name='user_head')
    op.drop_table('user_head')
    op.drop_index(op.f('ix_leave_start_date'), table_name='leave')
    op.drop_index(op.f('ix_leave_id'), table_name='leave')
    op.drop_index(op.f('ix_leave_end_date'), table_name='leave')
    op.drop_table('leave')
    op.drop_index(op.f('ix_department_user_id'), table_name='department_user')
    op.drop_table('department_user')
    op.drop_index(op.f('ix_user_role_id'), table_name='user_role')
    op.drop_table('user_role')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_role_id'), table_name='role')
    op.drop_table('role')
    op.drop_index(op.f('ix_holidays_id'), table_name='holidays')
    op.drop_index(op.f('ix_holidays_date'), table_name='holidays')
    op.drop_table('holidays')
    op.drop_index(op.f('ix_department_id'), table_name='department')
    op.drop_table('department')
    # ### end Alembic commands ###
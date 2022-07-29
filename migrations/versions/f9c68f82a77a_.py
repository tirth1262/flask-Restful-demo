"""empty message

Revision ID: f9c68f82a77a
Revises: 
Create Date: 2022-07-28 13:59:51.959370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9c68f82a77a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('firstname', sa.String(length=50), nullable=True),
    sa.Column('lastname', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('official_information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('join_date', sa.Date(), nullable=True),
    sa.Column('experience', sa.String(length=120), nullable=True),
    sa.Column('skype_id', sa.String(length=120), nullable=True),
    sa.Column('gitlab_id', sa.String(length=120), nullable=True),
    sa.Column('github_id', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_official_information_id'), 'official_information', ['id'], unique=False)
    op.create_table('personal_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blood_group', sa.String(length=20), nullable=True),
    sa.Column('marital_status', sa.String(length=20), nullable=True),
    sa.Column('emergency_number', sa.String(length=20), nullable=True),
    sa.Column('current_address', sa.Text(), nullable=True),
    sa.Column('permanent_address', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_personal_info_id'), 'personal_info', ['id'], unique=False)
    op.create_table('user_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=200), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_profile_id'), 'user_profile', ['id'], unique=False)
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_role_id'), 'user_role', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_role_id'), table_name='user_role')
    op.drop_table('user_role')
    op.drop_index(op.f('ix_user_profile_id'), table_name='user_profile')
    op.drop_table('user_profile')
    op.drop_index(op.f('ix_personal_info_id'), table_name='personal_info')
    op.drop_table('personal_info')
    op.drop_index(op.f('ix_official_information_id'), table_name='official_information')
    op.drop_table('official_information')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_role_id'), table_name='role')
    op.drop_table('role')
    # ### end Alembic commands ###
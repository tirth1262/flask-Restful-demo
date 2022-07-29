"""empty message

Revision ID: 81ec6e8be93b
Revises: f5e3e9b3f24a
Create Date: 2022-07-29 18:59:38.604219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ec6e8be93b'
down_revision = 'f5e3e9b3f24a'
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
    op.create_table('department_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('user_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_role_id'], ['role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_department_user_id'), 'department_user', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_department_user_id'), table_name='department_user')
    op.drop_table('department_user')
    op.drop_index(op.f('ix_department_id'), table_name='department')
    op.drop_table('department')
    # ### end Alembic commands ###

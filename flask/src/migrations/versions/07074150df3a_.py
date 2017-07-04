"""empty message

Revision ID: 07074150df3a
Revises: f80b0eb3bb58
Create Date: 2017-07-04 14:26:11.045423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07074150df3a'
down_revision = 'f80b0eb3bb58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=256, convert_unicode=True), nullable=False),
    sa.Column('email', sa.String(length=256, convert_unicode=True), nullable=False),
    sa.Column('password', sa.String(length=24), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('user_emails', 'profiles', ['email'], unique=True)
    op.create_index('usernames', 'profiles', ['username'], unique=True)
    op.add_column('tasks', sa.Column('profile_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'profiles', ['profile_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'profile_id')
    op.drop_index('usernames', table_name='profiles')
    op.drop_index('user_emails', table_name='profiles')
    op.drop_table('profiles')
    # ### end Alembic commands ###

"""agregando una tabla de password

Revision ID: 0d5f3505ae2f
Revises: f4ec92d7f01e
Create Date: 2023-05-18 20:31:16.441069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d5f3505ae2f'
down_revision = 'f4ec92d7f01e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_table('cameras_data')
    op.drop_table('passwords')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passwords',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('password', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cameras_data',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('fecha', sa.DATETIME(), nullable=True),
    sa.Column('imagen_base64', sa.TEXT(), nullable=False),
    sa.Column('camera_id', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('lastname', sa.VARCHAR(), nullable=False),
    sa.Column('age', sa.INTEGER(), nullable=True),
    sa.Column('disable', sa.BOOLEAN(), nullable=True),
    sa.Column('password_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['password_id'], ['passwords.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    # ### end Alembic commands ###
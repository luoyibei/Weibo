"""empty message

Revision ID: b8ac7509af53
Revises: 
Create Date: 2020-08-29 09:06:00.900747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8ac7509af53'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('u_name', sa.String(length=20), nullable=False),
    sa.Column('w_id', sa.Integer(), nullable=False),
    sa.Column('c_id', sa.Integer(), nullable=False),
    sa.Column('cmcontent', sa.Text(), nullable=False),
    sa.Column('cmtime', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_c_id'), 'comment', ['c_id'], unique=False)
    op.create_index(op.f('ix_comment_u_name'), 'comment', ['u_name'], unique=False)
    op.create_index(op.f('ix_comment_w_id'), 'comment', ['w_id'], unique=False)
    op.create_table('follow',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('f_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('u_id', 'f_id')
    )
    op.create_table('thumb',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('w_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('u_id', 'w_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('gender', sa.Enum('男', '女', '保密'), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('n_follow', sa.Integer(), nullable=False),
    sa.Column('n_fans', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_n_fans'), 'user', ['n_fans'], unique=False)
    op.create_index(op.f('ix_user_n_follow'), 'user', ['n_follow'], unique=False)
    op.create_table('wb',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('u_name', sa.String(length=20), nullable=False),
    sa.Column('n_thumb', sa.Integer(), nullable=False),
    sa.Column('wbtime', sa.DateTime(), nullable=False),
    sa.Column('wbcontent', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wb_n_thumb'), 'wb', ['n_thumb'], unique=False)
    op.create_index(op.f('ix_wb_u_id'), 'wb', ['u_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wb_u_id'), table_name='wb')
    op.drop_index(op.f('ix_wb_n_thumb'), table_name='wb')
    op.drop_table('wb')
    op.drop_index(op.f('ix_user_n_follow'), table_name='user')
    op.drop_index(op.f('ix_user_n_fans'), table_name='user')
    op.drop_table('user')
    op.drop_table('thumb')
    op.drop_table('follow')
    op.drop_index(op.f('ix_comment_w_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_u_name'), table_name='comment')
    op.drop_index(op.f('ix_comment_c_id'), table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###

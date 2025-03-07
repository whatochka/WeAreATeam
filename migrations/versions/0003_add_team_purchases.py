"""add team_purchases

Revision ID: 0003
Revises: 0002
Create Date: 2025-02-23 03:32:21.283856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0003'
down_revision: Union[str, None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team_purchases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['team_products.id'], name=op.f('fk_team_purchases_product_id_team_products'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_team_purchases_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_team_purchases'))
    )
    op.create_index(op.f('ix_team_purchases_id'), 'team_purchases', ['id'], unique=False)
    op.create_index(op.f('ix_team_purchases_product_id'), 'team_purchases', ['product_id'], unique=False)
    op.create_index(op.f('ix_team_purchases_user_id'), 'team_purchases', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_team_purchases_user_id'), table_name='team_purchases')
    op.drop_index(op.f('ix_team_purchases_product_id'), table_name='team_purchases')
    op.drop_index(op.f('ix_team_purchases_id'), table_name='team_purchases')
    op.drop_table('team_purchases')
    # ### end Alembic commands ###

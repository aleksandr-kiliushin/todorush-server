"""Added VerificationCode table

Revision ID: 26daf61761e9
Revises: 43388e6a5a77
Create Date: 2023-11-18 16:41:37.992064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26daf61761e9'
down_revision: Union[str, None] = '43388e6a5a77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verification_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=6), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verification_code')
    # ### end Alembic commands ###

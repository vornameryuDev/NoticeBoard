"""empty message

Revision ID: c036f781ac83
Revises: 318458bc5fa9
Create Date: 2024-07-02 17:26:04.866502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c036f781ac83'
down_revision: Union[str, None] = '318458bc5fa9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer', 'modify_date',
               existing_type=sa.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer', 'modify_date',
               existing_type=sa.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###

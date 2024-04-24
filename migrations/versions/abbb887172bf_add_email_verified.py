"""add email verified

Revision ID: abbb887172bf
Revises: a7b38ae91ebd
Create Date: 2024-04-16 15:32:37.817047

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "abbb887172bf"
down_revision: Union[str, None] = "a7b38ae91ebd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("email_verified", sa.Boolean(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "email_verified")
    # ### end Alembic commands ###
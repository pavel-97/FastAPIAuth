"""update user

Revision ID: 7644a1096444
Revises: 6d03284b2cd6
Create Date: 2023-11-24 17:16:54.485571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7644a1096444'
down_revision = '6d03284b2cd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
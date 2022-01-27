"""Create users table

Revision ID: 1cb6190d82d2
Revises: 
Create Date: 2022-01-27 08:32:26.561690

"""
import sqlalchemy as sa
from alembic import op
import sqlalchemy_utils as sa_u

# revision identifiers, used by Alembic.
revision = '1cb6190d82d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column("id", sa.Integer,
                              primary_key=True, nullable=False),
                    sa.Column("email", sa_u.EmailType, nullable=False, unique=True),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text("now()")))


def downgrade():
    op.drop_table('users')

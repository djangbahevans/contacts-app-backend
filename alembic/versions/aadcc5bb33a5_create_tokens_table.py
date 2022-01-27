"""create tokens table

Revision ID: aadcc5bb33a5
Revises: 2c82f7bb1ba2
Create Date: 2022-01-27 22:02:13.224274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aadcc5bb33a5'
down_revision = '2c82f7bb1ba2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("tokens",
                    sa.Column("id", sa.Integer,
                              primary_key=True, nullable=False),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey(
                        "users.id", ondelete="CASCADE"), nullable=False),
                    sa.Column("token", sa.String, nullable=False, unique=True),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))


def downgrade():
    op.drop_table("tokens")

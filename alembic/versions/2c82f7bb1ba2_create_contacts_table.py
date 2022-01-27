"""create contacts table

Revision ID: 2c82f7bb1ba2
Revises: 1cb6190d82d2
Create Date: 2022-01-27 08:57:08.502109

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as sa_u

# revision identifiers, used by Alembic.
revision = '2c82f7bb1ba2'
down_revision = '1cb6190d82d2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("contacts",
                    sa.Column("id", sa.Integer,
                              primary_key=True, nullable=False),
                    sa.Column("given_name", sa.String, nullable=True),
                    sa.Column("additional_name", sa.String, nullable=True),
                    sa.Column("family_name", sa.String, nullable=True),
                    sa.Column("name_prefix", sa.String, nullable=True),
                    sa.Column("name_suffix", sa.String, nullable=True),
                    sa.Column("birthday", sa.Date, nullable=True),
                    sa.Column("gender", sa.Enum("male", "female",
                              name="gender_enum"), nullable=True),
                    sa.Column("location", sa.String, nullable=True),
                    sa.Column("occupation", sa.String, nullable=True),
                    sa.Column("notes", sa.String, nullable=True),
                    sa.Column("photo", sa.String, nullable=True),
                    sa.Column("email", sa_u.EmailType, nullable=True),
                    sa.Column("phone1", sa_u.PhoneNumberType(), nullable=True),
                    sa.Column("phone2", sa_u.PhoneNumberType(), nullable=True),
                    sa.Column("organization", sa.String, nullable=True),
                    sa.Column("website", sa_u.URLType, nullable=True),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text("now()")),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))


def downgrade():
    op.drop_table("contacts")
    gender_enum = sa.Enum("male", "female", name="gender_enum")
    gender_enum.drop(op.get_bind())

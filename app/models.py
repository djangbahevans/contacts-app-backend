from sqlalchemy import TIMESTAMP, Boolean, Column, Date, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey

from .database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column("id", Integer, primary_key=True, nullable=False)
    given_name = Column("given_name", String, nullable=True)
    additional_name = Column("additional_name", String, nullable=True)
    family_name = Column("family_name", String, nullable=True)
    name_prefix = Column("name_prefix", String, nullable=True)
    name_suffix = Column("name_suffix", String, nullable=True)
    birthday = Column("birthday", Date, nullable=True)
    gender = Column("gender", Enum("male", "female", name="gender_enum"), nullable=True)
    location = Column("location", String, nullable=True)
    occupation = Column("occupation", String, nullable=True)
    notes = Column("notes", String, nullable=True)
    photo = Column("photo", String, nullable=True)
    email = Column("email", String, nullable=True)
    phone1 = Column("phone1", String, nullable=True)
    phone2 = Column("phone2", String, nullable=True)
    organization = Column("organization", String, nullable=True)
    website = Column("website", String, nullable=True)
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column("user_id", Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), nullable=False, server_default=text("now()"))

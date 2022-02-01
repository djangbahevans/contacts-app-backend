from sqlalchemy import (TIMESTAMP, Column, Date, Enum, ForeignKey, Integer,
                        String, Text, text)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from .database import Base

GenderEnum = Enum("male", "female", name="gender_enum")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column("id", Integer, primary_key=True, nullable=False)
    given_name = Column("given_name", String, nullable=True)
    additional_name = Column("additional_name", String, nullable=True)
    family_name = Column("family_name", String, nullable=True)
    name_prefix = Column("name_prefix", String, nullable=True)
    name_suffix = Column("name_suffix", String, nullable=True)
    birthday = Column("birthday", Date, nullable=True)
    gender = Column("gender", GenderEnum, nullable=True)
    location = Column("location", String, nullable=True)
    occupation = Column("occupation", String, nullable=True)
    notes = Column("notes", String, nullable=True)
    photo = Column("photo", Text, nullable=True)
    email = Column("email", EmailType, nullable=True)
    phone1 = Column("phone1", String(20), nullable=True)
    phone2 = Column("phone2", String(20), nullable=True)
    organization = Column("organization", String, nullable=True)
    website = Column("website", Text, nullable=True)
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column("user_id", Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, nullable=False)
    firstname = Column("firstname", String, nullable=False)
    lastname = Column("lastname", String, nullable=False)
    email = Column("email", EmailType, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), nullable=False, server_default=text("now()"))


class Token(Base):
    __tablename__ = "tokens"

    id = Column("id", Integer, primary_key=True, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    token = Column("token", String, nullable=False, unique=True)
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), nullable=False, server_default=text("now()"))

    owner = relationship("User")

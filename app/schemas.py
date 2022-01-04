from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    given_name: Optional[str] = None
    additional_name: Optional[str] = None
    family_name: Optional[str] = None
    name_prefix: Optional[str] = None
    name_suffix: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[GenderEnum] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
    notes: Optional[str] = None
    photo: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    organization: Optional[str] = None
    website: Optional[str] = None


class ContactCreate(ContactBase):
    ...


class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

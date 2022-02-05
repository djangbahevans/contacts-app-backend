from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, validator


class GenderEnum(str, Enum):
    male = 'male'
    female = 'female'


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: SecretStr

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[SecretStr]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
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
    photo: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    organization: Optional[str] = None
    website: Optional[HttpUrl] = None
    
    @validator("*", pre=True)
    def blank_string(cls, v):
        if v == "":
            return None
        return v
    
    @validator("gender", pre=True)
    def gender_lower(cls, v: str):
        if type(v) != str: return v
        return v.lower()


class ContactCreate(ContactBase):
    ...


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Email(BaseModel):
    email: EmailStr


class PasswordUpdate(BaseModel):
    password: SecretStr
    token: str

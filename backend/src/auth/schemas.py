from pydantic import BaseModel, Field
from datetime import datetime
from .model import UserType
from sqlalchemy import Enum
import uuid


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    user_type: str
    is_verified: bool
    is_active: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    user_type: UserType = Field(sa_column=Enum(UserType))


class UserUpdateModel(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class UserLoginModel(BaseModel):
    email: str
    password: str
from sqlalchemy import Enum
from enum import Enum as PyEnum
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


class UserType(PyEnum):
    ADMIN = 0
    TEACHER = 1
    STUDENT = 2


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str = Field(unique=True, nullable=False, max_length=10)
    email: str = Field(unique=True, nullable=False)
    first_name: str
    last_name: str
    user_type: str = Field(sa_column=Enum(UserType))
    is_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


    def __repr__(self):
        return f"<User {self.username}"

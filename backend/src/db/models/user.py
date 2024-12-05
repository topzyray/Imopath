import enum
from sqlmodel import SQLModel, Field
from datetime import datetime

class Role(enum.Enum):
    admin = 0
    teacher = 1
    student = 2

class User(SQLModel, table=True):
    __table__ = "users"

    id: str
    first_name: str
    last_name: str
    email: str
    password_hash: str
    role: Field(enum: Role)
    created_at: datetime
    updated_at: datetime
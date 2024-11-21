from fastapi import Depends, FastAPI # type: ignore
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select # type: ignore
from config import DATABASE_URL


class UserCreate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str


connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/signup")
def signup_user(user: UserCreate):
    # extract the data coming from req
    print(user.name)
    print(user.email)
    print(user.password)
    # check if the user already exixt in db
    # add user to db
    pass


from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting....")
    await init_db()
    yield
    print(f"Server has been stopped.")


version = "v1"


app = FastAPI(
    title="ImoPath",
    description="ImoPath an e-Learning Platform",
    version=version,
    lifespan=life_span
)


@app.get("/")
def root():
    return {"message": "ImoPath"}
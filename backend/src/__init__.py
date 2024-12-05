from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import initialize_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...")
    await initialize_db()
    yield
    print("Server has stopped.")


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
from fastapi import FastAPI

from backend.app.storage.database import db


async def lifespan(app: FastAPI):
    db.check_connection()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Привет мир"}

from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.routers import auth
from app.routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def read_root():
    return {"mensaje": "API funcionando"}

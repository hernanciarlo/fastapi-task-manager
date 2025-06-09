from fastapi import FastAPI
from app.routers import auth

from app.db.session import engine
from app.models import user
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def read_root():
    return {"mensaje": "API funcionando"}

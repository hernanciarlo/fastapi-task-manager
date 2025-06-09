from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agrego usuario y contraseña acá por ser un ejemplo simple. En producción usaría variables de entorno.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/taskdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

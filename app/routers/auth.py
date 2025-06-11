from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from collections.abc import Generator

from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import SessionLocal
from app.core.auth_utils import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)) -> dict[str, str | int]:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este email ya está registrado")

    nuevo_usuario = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario creado", "id": nuevo_usuario.id}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)) -> dict[str, str]:
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas"
        )

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(usuario_actual: User = Depends(get_current_user)) -> dict[str, str]:
    return {"email": usuario_actual.email}

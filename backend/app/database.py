
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Busca la configuración en backend/.env
RUTA_ENV = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(RUTA_ENV)


class Base(DeclarativeBase):
    """Clase base para los modelos de SQLAlchemy."""
    pass


DATABASE_URL = os.getenv("DATABASE_URL")

engine = (
    create_engine(DATABASE_URL)
    if DATABASE_URL
    else None
)

SessionLocal = (
    sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
    if engine
    else None
)


def get_db():
    """Entrega una sesión de base de datos por solicitud."""
    if SessionLocal is None:
        raise RuntimeError(
            "Configura DATABASE_URL en backend/.env"
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

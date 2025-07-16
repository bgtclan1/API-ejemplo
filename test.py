# Librerías estándar
import sqlite3  # para compatibilidad, aunque usaremos SQLAlchemy

# Librerías de terceros
from fastapi import FastAPI, HTTPException, Depends       # FastAPI y utilidades
from sqlalchemy import create_engine, Column, Integer, String, DateTime  # SQLAlchemy core
from sqlalchemy.ext.declarative import declarative_base  # Base de los modelos ORM
from sqlalchemy.orm import sessionmaker, Session          # Sesiones y tipado
from passlib.context import CryptContext                 # bcrypt hashing
from pydantic import BaseModel                           # para esquemas de entrada/salida
from typing import List                                  # para anotar List[UsuarioSchema]
from datetime import datetime                            # para timestamp por defecto

# Configuración base
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,    # No hacer commit automático
    autoflush=False,     # No vaciar al final de cada transacción
    bind=engine          # Vincula la sesión al engine creado
)
Base = declarative_base()

# Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  


def hash_password(plain_password: str) -> str:
    """Devuelve el hash bcrypt de la contraseña en texto plano."""
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña en texto plano coincida con el hash."""
    return pwd_context.verify(plain_password, hashed_password)



# Typeado Pydantic

class UsuarioSchema(BaseModel):
    id: int
    nombre: str
    email: str        
    fecha_creacion: datetime
    estado: int
    class Config:
        orm_mode = True
        # permite leer directamente atributos del ORM

class UsuarioCreate(BaseModel):
    nombre: str
    email: str      
    contraseña: str
    estado: int = 1   # valor por defecto

# Sesiones SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear tabla en la base de datos
Base.metadata.create_all(bind=engine)

# FastAPI
app = FastAPI()

# Endpoints

# @app.get("/",response_model=List[UsuarioSchema])
# async def get_all_users(db: Session = Depends(get_db)):
  
#     return  db.query(Usuario).all()

# @app.get("/{id}", response_model=UsuarioSchema)
# def get_user_by_id(id: int, db: Session = Depends(get_db)):
#     """
#     Devuelve un usuario por ID.
#     """
#     usuario = db.query(Usuario).filter(Usuario.id == id).first()
#     if not usuario:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
#     return usuario



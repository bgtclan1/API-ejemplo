# app/models.py

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    nombre: Mapped[str] = mapped_column(
        String, nullable=False, default=""
    )

    email: Mapped[str] = mapped_column(
        String, nullable=False, default=""
    )

    # ← Aquí el cambio clave: Mapped[str], no Column[str]
    contrasena_encriptada: Mapped[str] = mapped_column(
        String, nullable=False, default=""
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    estado: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )

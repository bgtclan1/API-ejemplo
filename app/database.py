from sqlalchemy import create_engine            # Crea el “engine” de la base de datos
from sqlalchemy.ext.declarative import declarative_base  # Clase base para definir modelos ORM
from sqlalchemy.orm import sessionmaker        # Fábrica de sesiones

DATABASE_URL = "sqlite:///./test.db"

# -------------------------------
#  Creación del Engine
# -------------------------------
# El engine gestiona el pool de conexiones y prepara las consultas
# connect_args={"check_same_thread": False} es necesario para SQLite y FastAPI (varios hilos)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# -------------------------------
# Configuración de las sesiones
# -------------------------------
# SessionLocal() nos dará instancias de Session ligadas al engine
# autocommit=False  -> no confirmar automáticamente cambios
# autoflush=False   -> no vaciar la sesión antes de cada commit
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# Todos los modelos ORM deberán heredar de esta clase
Base = declarative_base()

# -------------------------------
# Crear las tablas
# -------------------------------
# Si aún no existen, crea en la base de datos todas las tablas definidas
Base.metadata.create_all(bind=engine)

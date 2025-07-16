# app/main.py

from fastapi import FastAPI
from .routers import router as api_router  # importamos todos los endpoints

# Creamos la instancia de FastAPI
app = FastAPI()

# Montamos el router principal (todas las rutas definidas en routers.py)
app.include_router(api_router)

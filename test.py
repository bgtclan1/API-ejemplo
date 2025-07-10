from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db():
    conn = sqlite3.connect("test.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def get_all_users():
    db = get_db()
    users = db.execute("SELECT * FROM usuarios").fetchall()
    return users

@app.get("/{id}")
async def get_user_by_id(id: int):
    db = get_db()
    user = db.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()
    return user

# @app.get("/ping")
# async def getpong():
#     return {"respuesta": "pong"}  

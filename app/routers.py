from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .database import SessionLocal       
from .models import Usuario               
from .schemas import (
    UsuarioSchema,
    UsuarioCreate,
    LoginSchema,
    Token
)
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UsuarioSchema, status_code=201)
def register_user(
    payload: UsuarioCreate,
    db: Session = Depends(get_db)
):
    hashed = hash_password(payload.contraseña)        
    nuevo = Usuario(                                  
        nombre=payload.nombre,
        email=payload.email,
        contrasena_encriptada=hashed,
        estado=payload.estado
    )
    db.add(nuevo)                                     
    db.commit()                                      
    db.refresh(nuevo)                                 
    return nuevo   
    
@router.post("/login",response_model=str,status_code=201)
def login(
    credentials: LoginSchema,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.email == credentials.email
    ).first()                                        
    if not usuario or not verify_password(
        credentials.contraseña,
        usuario.contrasena_encriptada
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )                                            


    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(expires)
    token = create_access_token(
        data={"email": usuario.email},
        expires_delta=expires
    )                                                

    return token

@router.post("/", response_model=List[UsuarioSchema], status_code=201)
def get_all_users(
      token: Token, 
    db: Session = Depends(get_db)
):
    payload = decode_token(token.token)
    print(payload)
    return db.query(Usuario).all()


@router.post("/{id}", response_model=UsuarioSchema)

def get_user_by_id(
    token: Token,
    id: int,       
    db: Session = Depends(get_db)
):
    payload = decode_token(token.token)

    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
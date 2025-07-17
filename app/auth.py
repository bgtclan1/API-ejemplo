from datetime import datetime, timedelta        
from passlib.context import CryptContext       
import jwt                                      
from jwt import ExpiredSignatureError, InvalidTokenError
from functools import wraps
from fastapi import Depends, HTTPException , Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


SECRET_KEY = "S3mi7_Cl4v3_S3cr3t4"       
ALGORITHM = "HS256"                           
ACCESS_TOKEN_EXPIRE_MINUTES = 58              

def create_access_token(data: dict, expires_delta: timedelta ) -> str:
    to_encode = data.copy()
    now = datetime.now()
    to_encode.update({"iat": now})
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    #to_encode.update({"exp": expire})
    print(expire)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
    
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def token_required(func):
    @wraps(func)
    async def wrapper(
        *args,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        **kwargs
    ):
        print(credentials)
        token = credentials.credentials       
        payload = decode_token(token)         
        return await func(*args, token_data=payload, **kwargs)
    return wrapper
from pydantic import BaseModel, ConfigDict
from datetime import datetime    


class UsuarioSchema(BaseModel):
    id: int                        
    nombre: str                    
    email: str                     
    fecha_creacion: datetime       
    estado: int                    

    model_config = ConfigDict(from_attributes=True)
     

class UsuarioCreate(BaseModel):
    nombre: str                    
    email: str                     
    contraseña: str                
    estado: int = 1                


class LoginSchema(BaseModel):
    email: str                     
    contraseña: str                

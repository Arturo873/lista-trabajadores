# src/schemas/user_schema.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# schemas/user.py

from pydantic import BaseModel

class UserResponse(BaseModel):
    usuario: str
    cargo: str
    id_cargo:int
    class Config:
        from_attributes = True  # si usas Pydantic v2

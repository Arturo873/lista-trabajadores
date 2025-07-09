"""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from models.empleado_model import Empleado
from database.connection import get_db  # Asegúrate de tener esta función
from schemas.user_schema import UserResponse
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Empleado).filter(Empleado.usuario == username).first()
    if user is None:
        raise credentials_exception

    return UserResponse(usuario=user.usuario, cargo=user.cargo.nombre_cargo,id_cargo=user.cargo.id_cargo)


"""
def permiso_por_cargo(roles_permitidos: list[int]):
    def verificar(current_user: Empleado = Depends(get_current_user)):
        if current_user.id_cargo not in roles_permitidos:
            raise HTTPException(status_code=403, detail="No tienes permiso para esta operación")
        return current_user
    return Depends(verificar)
"""
from fastapi import Depends, HTTPException

def permiso_por_cargo(roles: list[int]):
    def verificar(user: UserResponse = Depends(get_current_user)):
        if user.id_cargo not in roles:
            raise HTTPException(status_code=403, detail="No autorizado")
        return user
    return verificar
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.empleado_model import Empleado
from models.cargo_model import Cargo
from sqlalchemy import or_
from models.empleado_model import Empleado  # importa tu modelo Empleado
from schemas.empleado_schema import EmpleadoCreate 
from schemas.empleado_schema import EmpleadoUpdate
from models.user_model import User
from typing import Optional
from fastapi import Query
from schemas.user_schema import UserResponse

from middleware.auth_middleware import get_current_user,permiso_por_cargo

#from schemas import UserCreate, UserLogin# Define esquemas Pydantic para validación
from database import get_db  # Función para obtener la sesión de DB
#from services.auth_services import get_password_hash, verify_password, create_access_token
from services.auth_services import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscar empleado por usuario o rut
    empleado = db.query(Empleado).filter(
        or_(
            Empleado.usuario == form_data.username,
            Empleado.rut == form_data.username
        )
    ).first()

    if not empleado or empleado.contrasena != form_data.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": empleado.usuario})
    return {"access_token": token, "token_type": "bearer"}

#--------------------------------JEFE RECURSOS HUMANOS
@router.get("/empleados/filtrar")
def filtrar_empleados(
    sexo: Optional[str] = Query(None),
    id_cargo: Optional[int] = Query(None),
    id_area: Optional[int] = Query(None),
    id_departamento: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = permiso_por_cargo([1]),
    user: UserResponse = Depends(permiso_por_cargo([1, 3]))
):
    query = db.query(Empleado)

    if sexo:
        query = query.filter(Empleado.sexo == sexo)
    if id_cargo is not None:
        query = query.filter(Empleado.id_cargo == id_cargo)
    if id_area is not None:
        query = query.filter(Empleado.id_area == id_area)
    if id_departamento is not None:
        query = query.filter(Empleado.id_departamento == id_departamento)

    empleados = query.all()

    if not empleados:
        raise HTTPException(status_code=404, detail="No se encontraron empleados con esos filtros")

    return empleados

#--------------------------------PERSONAL RR HH
@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def register(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    # Verificar si usuario o rut ya existe
    existing_empleado = db.query(Empleado).filter(
        or_(
            Empleado.usuario == empleado.usuario,
            Empleado.rut == empleado.rut
        )
    ).first()
    if existing_empleado:
        raise HTTPException(status_code=400, detail="El usuario o RUT ya está registrado")

    new_empleado = Empleado(
        rut=empleado.rut,
        nombre=empleado.nombre,
        genero=empleado.genero,
        direccion=empleado.direccion,
        telefono=empleado.telefono,
        fecha_ingreso=empleado.fecha_ingreso,
        id_cargo=empleado.id_cargo,
        usuario=empleado.usuario,
        contrasena=empleado.contrasena,
        fecha_despido=empleado.fecha_despido
    )
    db.add(new_empleado)
    db.commit()
    db.refresh(new_empleado)
    return {"msg": "Empleado registrado exitosamente"}

#--------------------------------EMPLEADOS
@router.get("/listarEmpleados")
def mostrar_empleados(db: Session = Depends(get_db)):
    empleados = db.query(Empleado).all()
    return empleados






"""
router = APIRouter(
    prefix="/empleados",
    tags=["empleados"]
)
"""





@router.get("/empleado{id}")
def obtener_empleado(id: int, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id).first()
    if not empleado:
        return {"error": "Empleado no encontrado"}
    return empleado


@router.put("/empleado/{id}")
def actualizar_empleado(id: int, datos: EmpleadoUpdate, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Solo actualizar si el valor no es el string por defecto "string"
    for campo, valor in datos.dict(exclude_unset=True).items():
        if valor is not None and valor != "string":
            setattr(empleado, campo, valor)

    db.commit()
    db.refresh(empleado)
    return {"mensaje": "Empleado actualizado", "empleado": empleado}




#permite al usuario ver su nombre y cargo
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.get("/endpoint-protegido")
async def endpoint(user: UserResponse = Depends(permiso_por_cargo([1, 3]))):
    return {"msg": "Acceso concedido", "user": user}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.empleado_model import Empleado
from models.cargo_model import Cargo
from sqlalchemy import or_
from models.empleado_model import Empleado  # importa tu modelo Empleado
from schemas.contacto_emergencia_schema import ContactoEmergenciaCreate
from schemas.empleado_schema import EmpleadoCreate,EmpleadoPerfil,EmpleadoUpdate
from schemas.carga_familiar_schema import CargaFamiliarUpdate,CargaFamiliarCreate


from models.carga_familiar_model import CargaFamiliar
from models.contacto_emergencia_model import ContactoEmergencia
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


#PERSONAL RR HH
@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def registrar(empleado: EmpleadoCreate, db: Session = Depends(get_db),
             user: UserResponse = Depends(permiso_por_cargo([2]))):
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
        contrasena=empleado.contrasena
        #fecha_despido=empleado.fecha_despido
    )
    db.add(new_empleado)
    db.commit()
    db.refresh(new_empleado)
    return {"msg": "Empleado registrado exitosamente"}

#JEFE 
@router.get("/empleados/filtrar")
def filtrar_empleados(
    sexo: Optional[str] = Query(None),
    id_cargo: Optional[int] = Query(None),
    id_area: Optional[int] = Query(None),
    id_departamento: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = permiso_por_cargo([1]),
    user: UserResponse = Depends(permiso_por_cargo([1]))
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


#jefe,RRHH y empleados
@router.get("/listarEmpleados")
def mostrar_empleados(db: Session = Depends(get_db),
                      user: UserResponse = Depends(permiso_por_cargo([1,2,3]))):
    empleados = db.query(Empleado).all()
    return empleados



#jefe,RRHH y empleados
@router.get("/empleados/miPerfil", response_model=EmpleadoPerfil)
def ver_mis_datos(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(permiso_por_cargo([1, 2, 3]))
):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == user.id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return EmpleadoPerfil(
        rut=empleado.rut,
        nombre=empleado.nombre,
        genero=empleado.genero,
        direccion=empleado.direccion,
        telefono=empleado.telefono,
        fecha_ingreso=empleado.fecha_ingreso,
        usuario=empleado.usuario,
        id_cargo=empleado.cargo.id_cargo,        
        cargo=empleado.cargo.nombre_cargo)





#JEFE y PERSONAL RRHH
#buscar empleado por id
@router.get("/empleado{id}")
def obtener_empleado(id: int, db: Session = Depends(get_db),
                     user: UserResponse = Depends(permiso_por_cargo([1, 2, ]))):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id).first()
    if not empleado:
        return {"error": "Empleado no encontrado"}
    return empleado


#PERSONAL RR HH
#actualizar empleado por id
@router.put("/actualizarEmpleado{id}")
def actualizar_empleado(id: int, datos: EmpleadoUpdate, db: Session = Depends(get_db),
                        user: UserResponse = Depends(permiso_por_cargo([2]))):
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



#jefe,RRHH y empleados
@router.put("/empleados/miPerfil")
def actualizar_mis_datos(
    datos_actualizados: EmpleadoUpdate,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(permiso_por_cargo([1, 2, 3]))
):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == user.id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Ignorar campos con valores "string", None o vacíos
    campos_validos = {
        key: value
        for key, value in datos_actualizados.dict(exclude_unset=True).items()
        if value is not None and value != "string" and (not isinstance(value, str) or value.strip() != "")
    }

    for key, value in campos_validos.items():
        setattr(empleado, key, value)

    db.commit()
    db.refresh(empleado)
    return {"mensaje": "Datos actualizados correctamente", "empleado": empleado}

#jefe,RRHH y empleados
@router.get("/empleados/mis-contactos-emergencia")
def ver_contactos_emergencia(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(permiso_por_cargo([1, 2, 3]))
):
    contactos = db.query(ContactoEmergencia).filter(ContactoEmergencia.id_empleado == user.id).all()
    if not contactos:
        raise HTTPException(status_code=404, detail="No se encontraron contactos de emergencia")
    return contactos


#jefe,RRHH y empleados
@router.get("/empleados/mis-cargas-familiares")
def ver_cargas_familiares(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(permiso_por_cargo([1, 2, 3]))
):
    cargas = db.query(CargaFamiliar).filter(CargaFamiliar.id_empleado == user.id).all()
    if not cargas:
        raise HTTPException(status_code=404, detail="No se encontraron cargas familiares")
    return cargas

#jefe,RRHH y empleados
@router.put("/cargafamiliar/{id_carga}")
def actualizar_carga_familiar(
    id_carga: int,
    data: CargaFamiliarUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    user: UserResponse = Depends(permiso_por_cargo([1, 2, 3]))
):
    carga = db.query(CargaFamiliar).filter(
        CargaFamiliar.id_carga == id_carga,
        CargaFamiliar.id_empleado == current_user.id
    ).first()

    if not carga:
        raise HTTPException(status_code=404, detail="Carga no encontrada o no autorizada")

    data_dict = data.dict(exclude_unset=True)
    for key, value in data_dict.items():
        if isinstance(value, str):
            # Ignora si es string vacío o string literal "string"
            if value.strip() == "" or value.strip().lower() == "string":
                continue
        setattr(carga, key, value)

    db.commit()
    db.refresh(carga)
    return {"message": "Carga actualizada correctamente", "carga": carga}
#RRHH 
@router.delete("/cargafamiliar/{id_carga}", status_code=204)
def eliminar_carga_familiar(
    id_carga: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    user: UserResponse = Depends(permiso_por_cargo([2,3]))
):
    carga = db.query(CargaFamiliar).filter(
        CargaFamiliar.id_carga == id_carga,
        CargaFamiliar.id_empleado == current_user.id  # ← igual aquí
    ).first()

    if not carga:
        raise HTTPException(status_code=404, detail="Carga familiar no encontrada o no autorizada")

    db.delete(carga)
    db.commit()
    return {"message": "eliminada con exito"}

#RRHH
@router.post("/cargafamiliar")
def crear_carga_familiar(
    data: CargaFamiliarCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    user: UserResponse = Depends(permiso_por_cargo([3]))
):
    data_dict = data.dict()

    # Filtrar campos vacíos o que sean "string"
    campos_validos = {
        k: v for k, v in data_dict.items()
        if v is not None and (not isinstance(v, str) or (v.strip() != "" and v.strip().lower() != "string"))
    }

    # Asegurarse de que hay campos válidos
    if not campos_validos:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos válidos")

    # Agregar el id_empleado del usuario logeado
    nueva_carga = CargaFamiliar(id_empleado=current_user.id, **campos_validos)

    db.add(nueva_carga)
    db.commit()
    db.refresh(nueva_carga)

    return {"message": "Carga familiar registrada correctamente", "carga": nueva_carga}


#RRHH
@router.delete("/eliminarEmpleado{id}", status_code=204)
def eliminar_empleado(
    id: int,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(permiso_por_cargo([2]))
):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id).first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    db.delete(empleado)
    db.commit()
    return {"message": "Empleado eliminado correctamente"}

@router.delete("/contactoemergencia{id_contacto}", status_code=204)
def eliminar_contacto_emergencia(
    id_contacto: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    user: UserResponse = Depends(permiso_por_cargo([1, 2, 3]))
):
    contacto = db.query(ContactoEmergencia).filter(
        ContactoEmergencia.id_contacto == id_contacto,
        ContactoEmergencia.id_empleado == current_user.id
    ).first()

    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto de emergencia no encontrado o no autorizado")

    db.delete(contacto)
    db.commit()
    return {"mensaje": "Contacto de emergencia eliminado correctamente"}



@router.post("/registrarContactoEmergencia", status_code=status.HTTP_201_CREATED)
def registrar_contacto_emergencia(
    contacto: ContactoEmergenciaCreate,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(permiso_por_cargo([3])) 
):
    # Asignar id_empleado del usuario logueado
    id_empleado_logueado = user.id

    # Verificar que el empleado existe
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado_logueado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    nuevo_contacto = ContactoEmergencia(
        id_empleado=id_empleado_logueado,
        nombre_contacto=contacto.nombre_contacto,
        relacion=contacto.relacion,
        telefono_contacto=contacto.telefono_contacto
    )

    db.add(nuevo_contacto)
    db.commit()
    db.refresh(nuevo_contacto)
    return {"mensaje": "Contacto de emergencia registrado correctamente", "id_contacto": nuevo_contacto.id_contacto}



"""
#permite al usuario ver su nombre y cargo
@router.get("/miCargo", response_model=UserResponse)
def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.get("/endpoint-protegido")
async def endpoint(user: UserResponse = Depends(permiso_por_cargo([1, 3]))):
    return {"msg": "Acceso concedido", "user": user}
"""
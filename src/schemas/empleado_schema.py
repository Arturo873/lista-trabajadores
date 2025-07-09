from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class GeneroEnum(str, Enum):
    M = "M"
    F = "F"
    Otro = "Otro"

class EmpleadoCreate(BaseModel):
    rut: str
    nombre: str
    genero: GeneroEnum
    direccion: str
    telefono: str
    fecha_ingreso: date
    id_cargo: int
    usuario: str
    contrasena: str
    fecha_despido: Optional[date] = None




class EmpleadoUpdate(BaseModel):
    nombre: Optional[str]
    usuario: Optional[str]
    id_cargo: Optional[int]
    telefono: Optional[str]
    class Config:
            #orm_mode = True
            from_attributes = True

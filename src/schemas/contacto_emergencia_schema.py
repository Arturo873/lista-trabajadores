from pydantic import BaseModel
from typing import Optional

class ContactoEmergenciaCreate(BaseModel):
   
    nombre_contacto: str
    relacion: str
    telefono_contacto: str

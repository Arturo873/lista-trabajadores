from pydantic import BaseModel
from typing import Optional, Literal


from pydantic import BaseModel, constr
from typing import Optional, Literal

class CargaFamiliarUpdate(BaseModel):
    nombre_carga: Optional[constr(strip_whitespace=True, max_length=100)]
    parentesco: Optional[constr(strip_whitespace=True, max_length=50)]
    genero_carga: Optional[Literal["M", "F", "Otro"]]
    rut_carga: Optional[constr(strip_whitespace=True, max_length=12)]

    class Config:
         from_attributes = True



class CargaFamiliarCreate(BaseModel):
    nombre_carga: Optional[str]
    parentesco: Optional[str]
    genero_carga: Optional[Literal['M', 'F', 'Otro']]
    rut_carga: Optional[str]


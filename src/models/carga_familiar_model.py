from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # asumiendo que tu Base está en database.py
import enum
class GeneroEnum(enum.Enum):
    M = "M"
    F = "F"
    Otro = "Otro"
class CargaFamiliar(Base):
    __tablename__ = "cargafamiliar"

    id_carga = Column(Integer, primary_key=True, autoincrement=True)
    id_empleado = Column(Integer, ForeignKey("empleado.id_empleado"), nullable=False)
    nombre_carga = Column(String(100), nullable=False)
    parentesco = Column(String(50), nullable=False)
    genero_carga = Column(Enum(GeneroEnum), nullable=False)
    rut_carga = Column(String(12), nullable=False)

    empleado = relationship("Empleado")
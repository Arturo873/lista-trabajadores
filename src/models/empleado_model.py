from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
#from database.connection import Base
from models.cargo_model import Cargo  
from database import Base
class Empleado(Base):
    __tablename__ = 'empleado'

    id_empleado = Column(Integer, primary_key=True)
    rut = Column(String(12), unique=True)
    nombre = Column(String(100))
    genero = Column(Enum('M', 'F', 'Otro'))
    direccion = Column(String(200))
    telefono = Column(String(15))
    fecha_ingreso = Column(Date)
    id_cargo = Column(Integer, ForeignKey("cargo.id_cargo"))
    usuario = Column(String(50), unique=True)
    contrasena = Column(String(255))
    fecha_despido = Column(Date, default=None)

    cargo = relationship("Cargo", back_populates="empleados")

    # Relaciones (ejemplo)
    # supervisor = relationship("Supervisor", back_populates="empleados")

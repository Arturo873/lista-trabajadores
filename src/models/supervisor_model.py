from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base
from models.empleado_model import Empleado  # Importa la clase Empleado
class Supervisor(Base):
    __tablename__ = 'supervisor'
    
    id_supervisor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)  # hay que aplicar hashing seguro
    permisos = Column(Enum('CRUD_TOTAL', name="permisos_enum"), nullable=False)

    # Relación con empleados
   #empleados = relationship("Empleado", backref="supervisor", cascade="all, delete-orphan")

    def __init__(self, nombre, usuario, contrasena):
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.permisos = 'CRUD_TOTAL'
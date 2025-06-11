from sqlalchemy import Column, Integer, String, Enum
from database.connection import Base

class TrabajadorRRHH(Base):
    __tablename__ = 'trabajador_rrhh'
    
    id_trabajador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)  # hay que ponerle hash mas adelante
    permisos = Column(Enum('AGREGAR_ACTUALIZAR', name="permisos_enum"), nullable=False)

    def __init__(self, nombre, usuario, contrasena):
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena  # Contraseña sin hash
        self.permisos = 'AGREGAR_ACTUALIZAR'
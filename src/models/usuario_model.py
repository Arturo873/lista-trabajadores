from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from database.connection import Base

class Trabajador(Base):
    __tablename__ = 'trabajador'
    
    id_trabajador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)  # Sin hashing por ahora
    permisos = Column(Enum('MODIFICAR_DATOS_PERSONALES', name="permisos_enum"), nullable=False)

    def __init__(self, nombre, usuario, contrasena):
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena  # Contraseña sin hash por ahora
        self.permisos = 'MODIFICAR_DATOS_PERSONALES'
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # asumiendo que tu Base está en database.py
import enum


class ContactoEmergencia(Base):
    __tablename__ = "contactoemergencia"

    id_contacto = Column(Integer, primary_key=True, autoincrement=True)
    id_empleado = Column(Integer, ForeignKey("empleado.id_empleado"), nullable=False)
    nombre_contacto = Column(String(100), nullable=False)
    relacion = Column(String(50), nullable=False)
    telefono_contacto = Column(String(15), nullable=False)

    empleado = relationship("Empleado")

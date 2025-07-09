from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Asegúrate de importar Base correctamente

class Cargo(Base):
    __tablename__ = "cargo"  # <- ¡Debe coincidir con el nombre exacto de tu tabla!

    id_cargo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_cargo = Column(String(50))
    id_permiso = Column(Integer, ForeignKey("Permiso.id_permiso"))
    id_area = Column(Integer, ForeignKey("Area.id_area"))

    # Relaciones (si están definidas)
    empleados = relationship("Empleado", back_populates="cargo")

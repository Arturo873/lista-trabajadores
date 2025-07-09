from sqlalchemy import Column, Integer, String
from database import Base

class Permiso(Base):
    __tablename__ = "permiso"

    id_permiso = Column(Integer, primary_key=True, index=True, autoincrement=True)
    modulo = Column(String(50))

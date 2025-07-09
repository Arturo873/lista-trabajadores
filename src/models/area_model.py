from sqlalchemy import Column, Integer, String
from database import Base

class Area(Base):
    __tablename__ = "area"

    id_area = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_area = Column(String(50))
    jefe_area = Column(String(100), nullable=True)

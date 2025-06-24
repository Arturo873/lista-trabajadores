from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Declarative Base para modelos
Base = declarative_base()

# Cadena de conexión SQLAlchemy (ajusta user/pass/host/db si es necesario)
DATABASE_URL = "mysql+mysqlconnector://root:@127.0.0.1/correo_de_yury"

# Crear el engine
engine = create_engine(DATABASE_URL)

# Crear session
Session = sessionmaker(bind=engine)
session = Session()

# Prueba opcional de conexión
def test_connection():
    try:
        with engine.connect() as conn:
            print("✅ Conexión exitosa a la base de datos (SQLAlchemy)")
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")

# Ejecuta test al importar
if __name__ == "__main__":
    test_connection()

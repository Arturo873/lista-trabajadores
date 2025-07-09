import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify

from datetime import datetime, timedelta
#from database.connection import create_connection
from models.usuario_model import Trabajador  # Modelo de trabajador

from routes.supervisor_routes import supervisor_bp
from routes.trabajador_routes import trabajador_bp
from routes.auth_routes import auth_bp  # Si tienes este blueprint

from database.connection import session
#import jwt
from jose import JWTError, jwt

from datetime import datetime, timedelta
# Clave secreta para JWT (debe ser la misma en toda la app)
SECRET_KEY = "Serenita lo mas grande"

# Crear la app Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Registrar blueprints
app.register_blueprint(supervisor_bp)
app.register_blueprint(trabajador_bp)
app.register_blueprint(auth_bp)




# -------------------------
# LOGIN POR CONSOLA (opcional)
# -------------------------
from models.empleado_model import Empleado  # Ajusta según el nombre real de tu archivo y clase

def login_por_consola():
    print("\n=== LOGIN POR CONSOLA ===")
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    

    try:
        empleado = session.query(Empleado).filter_by(usuario=usuario).first()

        if not empleado:
            print("❌ Usuario no encontrado.")
            return

        if empleado.contrasena != contrasena:
            print("❌ Contraseña incorrecta.")
            return

        permisos = "CRUD_TOTAL" if empleado.id_cargo == 1 else "VER_PROPIO"

        SECRET_KEY = "Serenita lo mas grande"

        token = jwt.encode({
            "id_empleado": empleado.id_empleado,
            "rut": empleado.rut,
            "permisos": permisos,
            "exp": datetime.utcnow() + timedelta(hours=4)
        }, SECRET_KEY, algorithm="HS256")

        print("\n✅ Login exitoso")
        print("🔑 Token generado:")
        print(token)
        return token

    except Exception as e:
        print(f"❌ Ocurrió un error durante el login: {e}")

# -------------------------
# MAIN
# -------------------------
"""
#esto ejecuta el main en bucle
if __name__ == "__main__":
    login_por_consola()  # ← Ejecuta login desde consola
    app.run(debug=True)
"""
#aqui se ejecuta la funcion una sola vezs
login_por_consola()
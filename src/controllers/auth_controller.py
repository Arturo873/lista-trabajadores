from flask import Blueprint, request, jsonify
import jwt
import datetime
from database.connection import session
from models.supervisor_model import Supervisor
from models.trabajador_model import TrabajadorRRHH
from models.usuario_model import Trabajador

# Clave secreta para firmar los tokens (mantén esto seguro)
SECRET_KEY = "Serenita lo mas grande"

# Crear un blueprint para autenticación
auth_bp = Blueprint("auth", __name__)

def generar_token(usuario, permisos):
    payload = {
        "usuario": usuario,
        "permisos": permisos,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # Token expira en 3 horas
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    contrasena = data.get("contrasena")

    # Buscar usuario en las tablas
    usuario_obj = session.query(Supervisor).filter_by(usuario=usuario).first() or \
                  session.query(TrabajadorRRHH).filter_by(usuario=usuario).first() or \
                  session.query(Trabajador).filter_by(usuario=usuario).first()

    if usuario_obj and usuario_obj.contrasena == contrasena:  # Sin hashing por ahora
        token = generar_token(usuario_obj.usuario, usuario_obj.permisos)
        return jsonify({"mensaje": "Login exitoso", "token": token})

    return jsonify({"error": "Credenciales incorrectas"}), 401

@auth_bp.route("/verificar_token", methods=["GET"])
def verificar_token():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token no proporcionado"}), 403

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"mensaje": "Token válido", "usuario": decoded_token["usuario"], "permisos": decoded_token["permisos"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401
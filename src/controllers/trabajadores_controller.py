from flask import Blueprint, request, jsonify
import jwt
from database.connection import session
from models.usuario_model import Trabajador
from functools import wraps
#from auth_controller import SECRET_KEY
from controllers.auth_controller import SECRET_KEY

# Crear blueprint para trabajadores
trabajador_bp = Blueprint("trabajador", __name__)

# Middleware para verificar JWT válido (sin exigir permisos especiales)
def verificar_trabajador(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token no proporcionado"}), 403

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token  # Guardamos el usuario decodificado
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated_function

# Obtener perfil del trabajador autenticado
@trabajador_bp.route("/mi-perfil", methods=["GET"])
@verificar_trabajador
def obtener_mi_perfil():
    rut_usuario = request.user.get("rut")
    trabajador = session.query(Trabajador).filter_by(rut=rut_usuario).first()

    if not trabajador:
        return jsonify({"error": "Trabajador no encontrado"}), 404

    return jsonify({
        "id_empleado": trabajador.id_empleado,
        "nombre": trabajador.nombre,
        "rut": trabajador.rut,
        "genero": trabajador.genero,
        "direccion": trabajador.direccion,
        "telefono": trabajador.telefono,
        "fecha_ingreso": trabajador.fecha_ingreso.isoformat() if trabajador.fecha_ingreso else None,
        "usuario": trabajador.usuario,
        "id_cargo": trabajador.id_cargo,
        "fecha_despido": trabajador.fecha_despido.isoformat() if trabajador.fecha_despido else None
    })

# Permitir actualización de su propio perfil (sin cambiar usuario ni contraseña)
@trabajador_bp.route("/mi-perfil", methods=["PUT"])
@verificar_trabajador
def actualizar_mi_perfil():
    rut_usuario = request.user.get("rut")
    trabajador = session.query(Trabajador).filter_by(rut=rut_usuario).first()

    if not trabajador:
        return jsonify({"error": "Trabajador no encontrado"}), 404

    data = request.json
    campos_actualizables = ["nombre", "direccion", "telefono", "genero"]

    for campo in campos_actualizables:
        if campo in data:
            setattr(trabajador, campo, data[campo])

    session.commit()
    return jsonify({"mensaje": "Perfil actualizado correctamente"})

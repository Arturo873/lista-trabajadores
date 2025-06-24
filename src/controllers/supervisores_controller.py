from flask import Blueprint, request, jsonify
import jwt
from database.connection import session
from models.usuario_model import Trabajador
from functools import wraps
#from auth_controller import SECRET_KEY
from controllers.auth_controller import SECRET_KEY

# Crear un blueprint para el Supervisor
supervisor_bp = Blueprint("supervisor", __name__)

# Middleware para verificar JWT y permisos

def verificar_supervisor(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token no proporcionado"}), 403

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if decoded_token["permisos"] != "CRUD_TOTAL":
                return jsonify({"error": "Acceso denegado"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorated_function

# Crear un nuevo empleado
@supervisor_bp.route("/empleados", methods=["POST"])
@verificar_supervisor
def agregar_empleado():
    data = request.json
    nuevo_empleado = Trabajador(
        nombre=data["nombre"],
        usuario=data["usuario"],
        contrasena=data["contrasena"],  # Sin hashing por ahora
        rut=data["rut"],
        genero=data["genero"],
        direccion=data["direccion"],
        telefono=data["telefono"],
        fecha_ingreso=data["fecha_ingreso"],
        id_cargo=data["id_cargo"]
    )
    session.add(nuevo_empleado)
    session.commit()
    return jsonify({"mensaje": "Empleado agregado exitosamente"})

# Actualizar datos de un empleado
@supervisor_bp.route("/empleados/<int:id>", methods=["PUT"])
@verificar_supervisor
def actualizar_empleado(id):
    data = request.json
    empleado = session.query(Trabajador).filter_by(id_empleado=id).first()

    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404

    for key, value in data.items():
        setattr(empleado, key, value)

    session.commit()
    return jsonify({"mensaje": f"Empleado {id} actualizado correctamente"})

# Eliminar un empleado
@supervisor_bp.route("/empleados/<int:id>", methods=["DELETE"])
@verificar_supervisor
def eliminar_empleado(id):
    empleado = session.query(Trabajador).filter_by(id_empleado=id).first()

    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404

    session.delete(empleado)
    session.commit()
    return jsonify({"mensaje": f"Empleado {id} eliminado correctamente"})

# Obtener todos los empleados
@supervisor_bp.route("/empleados", methods=["GET"])
@verificar_supervisor
def obtener_empleados():
    empleados = session.query(Trabajador).all()
    empleados_json = [{"id": e.id_empleado, "nombre": e.nombre, "usuario": e.usuario, "rut": e.rut} for e in empleados]
    return jsonify(empleados_json)
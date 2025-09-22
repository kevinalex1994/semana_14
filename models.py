from flask_login import UserMixin
from conexion.conexion import get_connection

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        data = cursor.fetchone()
        conn.close()
        if data:
            return Usuario(data['id_usuario'], data['nombre'], data['email'], data['password'])
        return None

    @staticmethod
    def obtener_por_id(id_usuario):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        data = cursor.fetchone()
        conn.close()
        if data:
            return Usuario(data['id_usuario'], data['nombre'], data['email'], data['password'])
        return None

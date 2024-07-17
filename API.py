import os
import psycopg2
from flask import Flask, jsonify, request, render_template, make_response
from datetime import datetime

app = Flask(__name__)

# Definimos una función con la que se realiza la conexión a la base de datos:
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "Database_API"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "docker"),
            host=os.getenv("DB_HOST", "db"),  # Cambiado de localhost a db
            port=os.getenv("DB_PORT", "5432"),
        )
        return conn
    except Exception as e:
        raise Exception(f"Error de conexión a la base de datos: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

# Función para crear un usuario y almacenarlo en la base de datos
# Se requiere que el usuario proporcione los mensajes en formato json. Ejemplo:

# {
#    Usuario = "rafa"
#    Correo = "rafa@gmail.com"
#    Mensaje = "hola" (opcional)
# }

@app.route("/users/register/", methods=['POST'])
def user_register():
    # Se obtienen los datos del POST
    if request.content_type == 'application/json':
        datos = request.json
    else:
        datos = request.form

    username = datos.get('Usuario')
    mail = datos.get('Correo')
    message = datos.get('Mensaje', '')  # Se pone un valor predeterminado vacío por defecto ''
    # La fecha se tiene en cuenta cuando se llama a esta función, no hace falta que la proporcione el usuario
    date = datetime.now().strftime("%Y-%m-%d")

    conn = get_db_connection()
    cursor = conn.cursor()  # Se crea un cursor para hacer consultas SQL

    if not username or not mail:
        return make_response("Usuario y mail son obligatorios", 400)

    # Comprobar si el usuario ya está registrado
    cursor.execute("SELECT id FROM Tabla_usuarios WHERE nombreUsuario = %s", (username,))
    user_exists = cursor.fetchone()

    if user_exists:
        return make_response("El usuario ya está registrado", 400)

    try:
        # Registramos nombre de usuario y email en la tabla de datos "usuarios"
        cursor.execute("INSERT INTO Tabla_usuarios (nombreUsuario, correoUsuario) VALUES (%s, %s)", (username, mail))
        conn.commit()
        # Registramos el mensaje asociado al USUARIO REGISTRADO en la tabla de datos "mensajes"
        # Para ello, extraemos el id asociado al USUARIO REGISTRADO en la base de datos.
        cursor.execute("SELECT id FROM Tabla_usuarios WHERE nombreUsuario = %s", (username,))
        user_ID = cursor.fetchone()[0]
        # Una vez seleccionado el ID del usuario, se guarda el mensaje asociado a dicho ID en la tabla de datos Mensajes
        cursor.execute("INSERT INTO Tabla_mensajes (IDusuario, mensaje, fecha) VALUES (%s, %s, %s)", (user_ID, message, date))
        conn.commit()

        return make_response("Registro exitoso", 200)
    except Exception as e:
        conn.rollback()
        return make_response(f"Error al registrar: {str(e)}", 500)
    finally:
        cursor.close()
        conn.close()

# Función para conseguir los comentarios publicados de un usuario en la base de datos
@app.route("/users/<username>/messages/", methods=['GET'])
def get_messages(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT mensaje FROM Tabla_mensajes WHERE IDusuario = (SELECT id FROM Tabla_usuarios WHERE nombreUsuario = %s)", (username,))
        listaOcurrencias = cursor.fetchall()
        listaMensajes = [fila[0] for fila in listaOcurrencias]

        if not listaMensajes:
            return make_response(f"No se encontraron mensajes para el usuario {username}", 404)

        # Devolver el resultado en formato texto plano:
        return make_response("Mensajes de {}: {}".format(username, ", ".join(listaMensajes)), 200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)
    finally:
        cursor.close()
        conn.close()

# Función para obtener una lista de todos los usuarios:
@app.route("/users/lista/", methods=['POST'])
def get_userlist():
    try:
        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta SQL para seleccionar todos los nombres de usuario
        cursor.execute("SELECT nombreUsuario FROM Tabla_usuarios")
        # Guardamos todas las filas que contienen nombre de usuario
        listaOcurrencias = cursor.fetchall()
        # Nos quedamos únicamente con el nombre de usuario
        listaUsuarios = [fila[0] for fila in listaOcurrencias]

        return make_response("Lista de usuarios: {}".format(", ".join(listaUsuarios)), 200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)
    finally:
        cursor.close()
        conn.close()

# Función para publicar un comentario como usuario:
# Se debe proporcionar el usuario y el mensaje en formato tipo json:
# {
#     Usuario: "rafa"
#     Mensaje: "mensaje publicado 1"
# }
@app.route("/users/publish/", methods=['POST'])
def publish_message():
    if request.content_type == 'application/json':
        datos = request.json
    else:
        datos = request.form

    user = datos.get('Usuario')
    message = datos.get('Mensaje')
    # La fecha la guardamos nosotros
    date = datetime.now().strftime("%Y-%m-%d")

    if not user or not message:
        return make_response("Usuario y mensaje son obligatorios", 400)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Tabla_usuarios WHERE nombreUsuario = %s", (user,))
        ID = cursor.fetchone()

        if ID is not None:
            ID = ID[0]
        else:
            return make_response("Usuario no encontrado", 404)

        cursor.execute("INSERT INTO Tabla_mensajes (IDusuario, mensaje, fecha) VALUES (%s, %s, %s)", (ID, message, date))
        conn.commit()

        return make_response("Mensaje publicado", 200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

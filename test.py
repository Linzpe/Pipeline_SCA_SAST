import unittest
import json
from API import API, get_db_connection

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.API = API.test_client()
        self.API.testing = True

        # Configuración de la base de datos para pruebas
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Tabla_usuarios (id SERIAL PRIMARY KEY, nombreUsuario VARCHAR(50) NOT NULL, correoUsuario VARCHAR(50) NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Tabla_mensajes (id SERIAL PRIMARY KEY, IDusuario INTEGER REFERENCES Tabla_usuarios(id), mensaje TEXT NOT NULL, fecha DATE NOT NULL)")
        conn.commit()
        cursor.close()
        conn.close()

    def tearDown(self):
        # Eliminar datos de las tablas después de las pruebas
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Tabla_mensajes")
        cursor.execute("DROP TABLE IF EXISTS Tabla_usuarios")
        conn.commit()
        cursor.close()
        conn.close()

    def test_user_register(self):
        # Prueba de registro de usuario
        response = self.API.post('/users/register/', data=json.dumps({
            "Usuario": "rafa",
            "Correo": "rafa@gmail.com"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registro exitoso", response.data)

    def test_get_messages(self):
        # Registrar un usuario primero
        self.API.post('/users/register/', data=json.dumps({
            "Usuario": "rafa",
            "Correo": "rafa@gmail.com"
        }), content_type='application/json')

        # Publicar un mensaje
        self.API.post('/users/publish/', data=json.dumps({
            "Usuario": "rafa",
            "Mensaje": "Hola, este es un mensaje de prueba"
        }), content_type='application/json')

        # Prueba de obtención de mensajes del usuario
        response = self.API.get('/users/rafa/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hola, este es un mensaje de prueba", response.data)

    def test_publish_message(self):
        # Registrar un usuario primero
        self.API.post('/users/register/', data=json.dumps({
            "Usuario": "rafa",
            "Correo": "rafa@gmail.com"
        }), content_type='application/json')

        # Prueba de publicación de un mensaje
        response = self.API.post('/users/publish/', data=json.dumps({
            "Usuario": "rafa",
            "Mensaje": "Hola, este es otro mensaje de prueba"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mensaje publicado", response.data)

if __name__ == '__main__':
    unittest.main()

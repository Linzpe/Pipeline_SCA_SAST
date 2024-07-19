import unittest
from unittest.mock import patch, MagicMock
import json
from API import app, get_db_connection

class FlaskTestCase(unittest.TestCase): # Al heredar de TestCase, podemos definir métodos en la clase que representen casos de prueba individuales.

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    ## PRUEBA UNITARIA 1
    # El patch a continuación se usa para sustituir el ""objeto"" get_db_connection por un objeto simulado "MagicMock"
    @patch('API.get_db_connection')
    def test_user_register(self, mock_get_db_connection):
        # Crear un cursor y conexión falsos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Configurar el comportamiento del cursor
        mock_cursor.fetchone.side_effect = [None, (1,)] # Significa que no hay ningún usuario registrado en la base de datos.

        # Se realiza el resgistro de un usuario
        response = self.app.post('/users/register/', data=json.dumps({
            "Usuario": "rafa",
            "Correo": "rafa@gmail.com"
        }), content_type='application/json')
        
        if response.status_code != 200:
            print(response.data)
        
        # Verificar el comportamiento y resultado
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registro exitoso", response.data)  # Busca si en "response.data" se encuentra "Registro Exitoso"
        print("Prueba de registro de usuario exitosa")
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()

    ## PRUEBA UNITARIA 2
    @patch('API.get_db_connection')
    def test_get_messages(self, mock_get_db_connection):
        # Crear un cursor y conexión falsos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Configurar el comportamiento del cursor
        mock_cursor.fetchall.return_value = [("Hola, este es un mensaje de prueba",)]

        # Realizar la petición GET
        response = self.app.get('/users/rafa/messages/')

        # Verificar el comportamiento y resultado
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hola, este es un mensaje de prueba", response.data)
        print("Prueba de obtencion de mensajes exitosa")
        mock_cursor.execute.assert_called()
    
    
    ## PRUEBA UNITARIA 3
    @patch('API.get_db_connection')
    def test_publish_message(self, mock_get_db_connection):
        # Crear un cursor y conexión falsos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Configurar el comportamiento del cursor
        mock_cursor.fetchone.return_value = [1]

        # Realizar la petición POST
        response = self.app.post('/users/publish/', data=json.dumps({
            "Usuario": "rafa",
            "Mensaje": "Hola, este es otro mensaje de prueba"
        }), content_type='application/json')

        # Verificar el comportamiento y resultado
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mensaje publicado", response.data)
        print("Prueba de publicación de mensaje exitosa")
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()

if __name__ == '__main__':
    unittest.main()

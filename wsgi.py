import sys
from API import app as application

# Asegúrate de que el directorio de la aplicación esté en la ruta de búsqueda
sys.path.insert(0, '/var/www/html/app')

if __name__ == "__main__":
    application.run()
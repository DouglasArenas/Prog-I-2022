#Instalar python3-venv para poder manejar entornos virtuales
#Importar librería os
import os
#Importar DotEnv para manejar variables de entorno
# from dotenv import load_dotenv
from main import create_app
#Cargar variables de entorno de archivo .env
app = create_app()
# load_dotenv()
#Inicializar aplicación Flask
app.app_context().push()
#Verificar que el script se este ejecutando directamente
if __name__ == '__main__':
    #Correr servidor web
    #Debug: Si está activado muestra mensajes de error y se reinicia al encontrar cambios
    #Port: Puerto en el que va a correr el servicio. Obtenido de las variables de entorno
    app.run(debug = True, port = os.getenv("PORT"))


import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources
api = Api()

#Método que inicializará todos los módulos y devolverá la aplicación
def create_app():
    #Inicializar Flask
    app = Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()
    #
    #Aquí se inicializarán el resto de los módulos de la aplicación
    api.add_resource(resources.QualificationResource, '/calificacion/<id>')
    api.add_resource(resources.QualificationsResource, '/calificaciones')
    api.add_resource(resources.PoemResource, '/poema/<id>')
    api.add_resource(resources.PoemsResource, '/poemas')
    api.add_resource(resources.UserResource, '/usuario/<id>')
    api.add_resource(resources.UsersResource, '/usuarios')

    #
    #Retornar aplicación inicializada
    api.init_app(app)
    return app


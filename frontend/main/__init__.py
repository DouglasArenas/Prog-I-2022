import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    #inicializar Flask
    app=Flask(__name__)
    
    #Cargar variables de entorno
    load_dotenv()

    #Cargar configuracion
    app.config['API_URL'] = os.getenv('API_URL')

    #Importar Blueprints
    from main.routes import main, poems, users, qualifications
    app.register_blueprint(main.app)
    app.register_blueprint(poems.poems)
    app.register_blueprint(users.users)
    app.register_blueprint(qualifications.qualifications)
        
    #retornar aplicaciion inicializada
    return app

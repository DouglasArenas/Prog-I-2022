import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager, login_required

login_manager = LoginManager()

def create_app():
    #inicializar Flask
    app=Flask(__name__, static_url_path='/static')
    
    #Cargar variables de entorno
    load_dotenv()

    #Cargar configuracion
    app.config['API_URL'] = os.getenv('API_URL')
    login_manager.init_app(app)

    #Importar Blueprints
    from main.routes import main
    app.register_blueprint(routes.main.app)
    
    
    #retornar aplicaciion inicializada
    return app

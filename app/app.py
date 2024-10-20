import sys
import os
from flask import Flask, render_template
from pymongo import MongoClient
from routes import user_routes  # Importar o Blueprint
from dotenv import load_dotenv
load_dotenv()

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# garantir que o diretório atual (/app) seja incluído no PYTHONPATH dentro do container.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    # Inicializar a aplicação Flask
    app = Flask(__name__)


    # Conectando ao MongoDB
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client.login
    
    # Registrando o Blueprint
    app.register_blueprint(user_routes)
    
    @app.route('/')
    def inicio():
        return render_template('inicio.html')


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
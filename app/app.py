from flask import Flask, redirect, render_template, request, url_for  # Adicionando render_template
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
load_dotenv()
import jwt  # Biblioteca para JWT
import datetime  # Para configurar expiração do token


# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# garantir que o diretório atual (/app) seja incluído no PYTHONPATH dentro do container.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Inicializando a aplicação Flask
app = Flask(__name__)

# Definindo a SECRET_KEY, com um valor padrão caso não esteja no ambiente
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key') 

# Conectando ao MongoDB
client = MongoClient(os.getenv('MONGO_URI'))
db = client.login

# Importando o Blueprint para as rotas de usuários
from routes import user_routes  # Certifique-se de que 'routes.py' está funcionando corretamente

# Registrando o Blueprint
app.register_blueprint(user_routes)

# Criando rota para a página inicial
@app.route('/')
def index():
    return render_template('inicio.html') 

@app.route('/login')
def login():
    return render_template('login.html')  # Renderiza o HTML da página login.html

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Renderiza o HTML da página dashboard.html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

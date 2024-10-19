# Importar a biblioteca Flask
from flask import Flask
# Importando o Blueprint para as rotas de usuários
from routes import user_routes

# Inicializar a aplicação Flask
app = Flask(__name__)

# Importando o Blueprint para as rotas de usuários
from routes import user_routes  # Certifique-se de que 'routes.py' está funcionando corretamente

# Registrando o Blueprint
app.register_blueprint(user_routes)

# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
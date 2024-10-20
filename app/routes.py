from flask import Blueprint, render_template, Flask

app = Flask(__name__)

user_routes = Blueprint('user_routes', __name__)

@app.route('/')
def users():
    return render_template('inicio.html')

@user_routes.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Registrar o Blueprint
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run()
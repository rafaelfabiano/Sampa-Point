from flask import Blueprint, current_app, render_template, Flask


user_routes = Blueprint('user_routes', __name__)
app = Flask(__name__)

if __name__ == "__main__":
    app.run()
    
    
@user_routes.route('/')
def users():
    return render_template('inicio.html')

@user_routes.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


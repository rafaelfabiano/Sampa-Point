from flask import Blueprint, current_app, render_template, Flask


user_routes = Blueprint('user_routes', __name__)
app = Flask(__name__)


# @user_routes.route('/')
# def inicio():
#     return render_template('inicio.html')


@user_routes.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')



app.register_blueprint(user_routes)
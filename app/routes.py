from flask import Blueprint, current_app
from flask import render_template

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/')
def users():
    return render_template('inicio.html')

@user_routes.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
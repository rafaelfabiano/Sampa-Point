from flask import Blueprint, current_app

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/')
def users():
    return "Hello, World!"

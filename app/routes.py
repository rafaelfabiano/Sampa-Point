from flask import Blueprint
from app import app
import os

# Criando um Blueprint
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def home():
    return "Hello, World!"

# auth_decorator.py
from functools import wraps
from bson import ObjectId
from flask import jsonify, request, redirect, url_for, flash, Blueprint, make_response, render_template
from datetime import datetime, timezone
import jwt
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregando o arquivo .env
load_dotenv()

# Conectar ao MongoDB
client = MongoClient(os.getenv('BD_AUTH')) #colocar a variável do arquivo env
users_db = client.login # Banco de dados para autenticação de usuários




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')  # Pegar o token do cookie

        if not token:
            # Se o token não for encontrado, redireciona para a página de erro
            return render_template('erro_login.html', error_message='Token não encontrado!'), 403

        try:
            # Decodificar o token JWT
            SECRET_KEY = os.getenv('SECRET_KEY_TOKEN')
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = users_db.users.find_one({"_id": ObjectId(data['user_id'])})

            if not current_user:
                # Se o usuário não for encontrado, renderizar a página de erro
                return render_template('erro_login.html', error_message='Usuário não encontrado!'), 403

        except jwt.ExpiredSignatureError:
            # Token expirado
            return render_template('erro_login.html', error_message='Token expirado!'), 403
        except jwt.InvalidTokenError:
            # Token inválido
            return render_template('erro_login.html', error_message='Token inválido!'), 403

        # Passar current_user e manter os outros argumentos intactos
        return f(current_user, *args, **kwargs)

    return decorated_function


def setor_required(allowed_roles):
    """Decorator para verificar se o usuário tem um dos cargos permitidos."""
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            user_role = current_user.get('setor')

            if not user_role:
                # Se o usuário não tem um papel definido, negamos o acesso
                return render_template('erro_login.html', error_message='Função não definida!'), 403

            if user_role not in allowed_roles:
                # Se o papel do usuário não está na lista de cargos permitidos
                return render_template('erro_login.html', error_message='Acesso negado! Você não tem permissão suficiente.'), 403

            # Se o usuário tem permissão, continue com a execução da função
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator


def nivel_required(required_nivel):
    """
    Decorator para verificar se o usuário tem o nível necessário ou superior.
    Usuários com nível inferior não podem acessar dados de níveis superiores.
    Usuários com nível superior podem acessar dados de níveis inferiores.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            user_nivel = current_user.get('nivel')

            if user_nivel is None:
                # Se o nível do usuário não está definido, nega o acesso
                return render_template('erro_login.html', error_message='Nível não definido!'), 403

            try:
                # Converte o nível do usuário para inteiro
                user_nivel = int(user_nivel)
            except ValueError:
                # Caso o nível do usuário não seja um número válido
                return render_template('erro_login.html', error_message='Nível de usuário inválido!'), 403

            if user_nivel < required_nivel:
                # Se o nível do usuário é inferior ao necessário, nega o acesso
                return render_template('erro_login.html', error_message='Acesso negado!'), 403

            # Se o usuário tem o nível necessário ou superior, continua a execução
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

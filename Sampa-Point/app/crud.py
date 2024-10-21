from pymongo import MongoClient
from bson import ObjectId
import bcrypt
from datetime import datetime, timezone
import os

# Inicializando conexão com o MongoDB diretamente aqui
client = MongoClient(os.getenv('MONGO_URI'))
db = client.sampapoint


def create_user(email, password, first_name, nascimento, celular, bairro, cidade):
    # Verificando se o email já existe no banco de dados
    existing_user = db.users.find_one({"email": email})
    if existing_user:
        raise ValueError("Este e-mail já está cadastrado.")
    
    # Criptografando a senha
    #password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Criando o novo usuário
    new_user = {
        "email": email,
        "password_hash": password,
        "first_name": first_name,
        "data_nascimento": nascimento,
        "celular": celular,
        "bairro": bairro,
        "cidade": cidade,
        "selos": 0,
        "checklist": [],
        "preferencias": {
            "cultural": 0,
            "gastronomico": 0,
            "negocios": 0,
            "compras": 0,
            "aventura": 0,
            "religioso": 0,
            "eventos": 0,
            "historico": 0
        }
    }
    # Inserindo no banco de dados
    result = db.users.insert_one(new_user)
    return result.inserted_id


def create_point(nome, endereco, acessibilidade, custos, estacoes, cidade, bairro, latitude, longitude, categoria):
    # Verificando se o email já existe no banco de dados
    # Criptografando a senha
    #password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Criando o novo usuário
    new_point = {
        "nome": nome,
        "categoria": categoria,
        "endereco": endereco,
        "acessibilidade": acessibilidade,
        "custos": custos,
        "estacoes": estacoes,
        "cidade": cidade,
        "bairro": bairro,
        "latitude": latitude,
        "longitude": longitude
    }
    # Inserindo no banco de dados
    result = db.points.insert_one(new_point)
    return result.inserted_id


def log_login_attempt(user_id, status, ip_address):
    # Cria o log da tentativa de login
    login_attempt = {
        "attempt_time": datetime.now(timezone.utc),
        "status": status,
        "ip_address": ip_address
    }

    # Insere o log no campo 'login_attempts' do usuário
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"login_attempts": login_attempt}}
    )


def get_user_by_email(email):
    # Retorna o usuário pelo email
    return db.users.find_one({"email": email})


def get_user_by_id(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user


def get_point_by_id(point_id):
    # Retorna o point pelo ID
    point = db.points.find_one({"_id": ObjectId(point_id)})
    print(f"Point encontrado: {point}")  # Log do ponto encontrado
    return point

def update_user(user_id, update_fields):
    # Atualizando o usuário no banco de dados
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})


def delete_user(user_id):
    # Remove um usuário com base no user_id
    db.users.delete_one({"_id": ObjectId(user_id)})

def get_all_users():
    users = db.users.find() 
    return list(users)

def get_all_points():
    points = db.points.find() 
    return list(points)

from flask import app
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a URI do MongoDB
MONGO_URI = os.getenv("MONGO_URI")
mongo = PyMongo()
mongo.init_app(app)

def criar_usuario(dados):
    mongo.db.usuarios.insert_one(dados)

def ler_usuarios():
    return mongo.db.usuarios.find()

def ler_usuario_por_id(id):
    return mongo.db.usuarios.find_one({'_id': ObjectId(id)})

def atualizar_usuario(id, dados):
    mongo.db.usuarios.update_one({'_id': ObjectId(id)}, {'$set': dados})

def deletar_usuario(id):
    mongo.db.usuarios.delete_one({'_id': ObjectId(id)})
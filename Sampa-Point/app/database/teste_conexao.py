import os
from pymongo import MongoClient

# Carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()

# Obter a URI do MongoDB da variável de ambiente
mongodb_uri = os.getenv('MONGO_URI')

# Conectar ao MongoDB
client = MongoClient(mongodb_uri)

# Verificar a conexão
try:
    client.admin.command('ping')
    print("Conectado ao MongoDB com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
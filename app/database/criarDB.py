from pymongo import MongoClient
from datetime import datetime

# Conectando ao MongoDB
client = MongoClient('mongodb://mongo:4e41495009b335692daf@85.31.231.38:27017')  # Substitua pela sua URI do MongoDB se for diferente
db = client.sampapoint# Substitua  pelo nome do seu banco de dados

# Definindo a coleção 'users'
users_collection = db.users

# Inserindo um novo usuário
new_user = {
    "username": "janedoe",
    "email": "janedoe@example.com",
    "password_hash": "$2b$12$DkYhssYzGuR5d...",  # Hash da senha gerada com bcrypt ou outra função de hash
    "role": "user",
    "permissions": ["view_profile", "edit_profile"],
    "created_at": datetime.utcnow(),  # Data atual
    "last_login": datetime.utcnow(),  # Último login (definido como agora)
    "is_active": True,  # Conta está ativa
    "mfa_enabled": False,  # Autenticação de múltiplos fatores desabilitada
    "profile": {
        "first_name": "Jane",
        "last_name": "Doe",
        "bio": "Graphic Designer at XYZ Corp",
        "avatar_url": "https://example.com/avatar/janedoe.jpg"
    },
    "login_attempts": [  # Tentativas de login anteriores
        {
            "attempt_time": datetime(2024, 9, 12, 14, 10, 0),
            "status": "failure",
            "ip_address": "192.168.0.10"
        },
        {
            "attempt_time": datetime(2024, 9, 12, 14, 20, 0),
            "status": "success",
            "ip_address": "192.168.0.10"
        }
    ]
}

# Inserindo o documento no banco de dados
result = users_collection.insert_one(new_user)

# Exibindo o ID do novo usuário inserido
print(f"Usuário inserido com ID: {result.inserted_id}")

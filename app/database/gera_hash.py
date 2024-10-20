import bcrypt

# Gerando o hash da senha
senha_plana = "minhasenha123"
password_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt())

print(password_hash.decode('utf-8'))

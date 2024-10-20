# Usar uma imagem base oficial do Python
FROM python:3.11.9-slim


# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta em que a aplicação irá rodar
EXPOSE 5000

# Comando para rodar a aplicação 
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
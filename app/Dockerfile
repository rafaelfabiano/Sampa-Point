FROM python:3.11.9-slim

WORKDIR /app

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar a aplicação para o contêiner
COPY . .

# Expor a porta que será usada 
EXPOSE 5000

# Comando para rodar a aplicação 
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

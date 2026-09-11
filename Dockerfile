# Imagem base oficial do Python (versão leve alpine)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia a lista de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto para dentro do container
COPY check_sistema.py .
COPY .env .

# Comando padrão a ser executado ao iniciar o container
CMD ["python", "check_sistema.py"]

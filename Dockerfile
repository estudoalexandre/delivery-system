# Use a imagem oficial do Python
FROM python:3.11

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências para o container
COPY requirements.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instale sqlite3
RUN apt-get update && apt-get install -y sqlite3

# Copie o restante do código do projeto para o container
COPY . /app/

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

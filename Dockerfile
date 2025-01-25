# Use a imagem oficial do Python
FROM python:3.11-slim-buster

# Defina a variável de ambiente para que a saída python seja enviada diretamente
# para o terminal sem ser primeiro armazenada em buffer.
ENV PYTHONUNBUFFERED=1

# Crie um diretório de trabalho no contêiner
WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libodbc1 \
    odbcinst \
    odbcinst1debian2 \
    curl \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt /app

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyodbc

# Copie o código do aplicativo para o contêiner
COPY . /app

# # Exponha a porta em que a aplicação será executada
# EXPOSE 8000

CMD ["fastapi", "run", "app", "--host", "0.0.0.0", "--port", "80"]
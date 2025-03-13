#!/bin/bash

# Diretório base do projeto
PROJECT_DIR="sensor-monitoring"

# Criar estrutura de diretórios
mkdir -p $PROJECT_DIR/{models,datasets,data}

# Criar o arquivo Dockerfile
cat <<EOL > $PROJECT_DIR/Dockerfile
# Usa uma imagem base do Python
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe as portas do servidor HTTP e da API
EXPOSE 8000 5000

# Comando para rodar múltiplos serviços no container
CMD ["sh", "-c", "python server.py data/ & python api.py"]
EOL

# Criar o arquivo docker-compose.yml
cat <<EOL > $PROJECT_DIR/docker-compose.yml
version: "3.8"
services:
  server:
    build: .
    container_name: sensor_server
    ports:
      - "8000:8000"
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - DATA_DIR=/app/data
EOL

# Criar o arquivo requirements.txt
cat <<EOL > $PROJECT_DIR/requirements.txt
fastapi
uvicorn
numpy
scipy
pandas
matplotlib
seaborn
scikit-learn
EOL

# Criar arquivos de código vazios
touch $PROJECT_DIR/{server.py,api.py,training.py,analysis.py}

# Exibir a estrutura criada
echo "Estrutura do projeto criada em $PROJECT_DIR"
tree $PROJECT_DIR

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

import os
import shutil

# Diretório base do projeto
PROJECT_NAME = "startup_one-2025"
BASE_DIR = os.path.expanduser(f"~/PycharmProjects/{PROJECT_NAME}")

# Estrutura correta do projeto
DIR_STRUCTURE = {
    "anomaly-detection": [],
    "anomaly-detection/esp32": [],
    "anomaly-detection/sensor-monitoring": ["sensor_data"],
    "anomaly-detection/tests": [],
    "anomaly-detection/models": [],
    "DataSheet-sensores": [],
    "Infrastructure-Provisioning": [],
    ".github/workflows": [],
}

# Arquivos essenciais
FILES = {
    ".gitignore": """# Ignorar arquivos desnecessários
venv/
__pycache__/
*.pyc
.DS_Store
.idea/
.env
logs/
""",
    "README.md": f"# {PROJECT_NAME}\n\nEste repositório contém a estrutura do projeto para detecção de anomalias.",
    "anomaly-detection/requirements.txt": """# Dependências do projeto
fastapi
uvicorn
numpy
scipy
requests
pytest
pydantic
""",
    "anomaly-detection/api.py": """# Código base da API (FastAPI)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API Running"}
""",
    "anomaly-detection/tests/test_api.py": """# Testes automatizados para a API
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API Running"}
""",
    "setup_docker_structure.sh": """#!/bin/bash
echo "Configurando ambiente Docker..."
docker-compose up -d --build
""",
    ".github/workflows/ci.yml": """name: Run Tests

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.9"

      - name: Install dependencies
        run: |
          pip install -r anomaly-detection/requirements.txt

      - name: Run tests
        run: pytest anomaly-detection/tests/
""",
}

# Diretórios que devem ser removidos
DIRS_TO_REMOVE = [
    "Infrastructure Provisioning",  # Nome corrigido para evitar erro
    "DataSheet-sensores",
    ".idea",
    "__pycache__",
    "venv",
    "logs"
]

# Arquivos que devem ser movidos para seus respectivos locais
FILES_TO_MOVE = {
    "setup_docker_structure.sh": BASE_DIR,
    "README.md": BASE_DIR,
    "requirements.txt": os.path.join(BASE_DIR, "anomaly-detection"),
    "api.py": os.path.join(BASE_DIR, "anomaly-detection"),
    "test_api.py": os.path.join(BASE_DIR, "anomaly-detection/tests"),
}


def remove_unnecessary_dirs():
    """Remove diretórios desnecessários de forma segura"""
    print("\n🗑️ Removendo diretórios desnecessários...")

    for directory in DIRS_TO_REMOVE:
        dir_path = os.path.join(BASE_DIR, directory)

        if os.path.exists(dir_path):
            if os.path.isdir(dir_path):  # Garante que é um diretório antes de remover
                shutil.rmtree(dir_path)
                print(f"✅ Diretório removido: {dir_path}")
            else:
                print(f"⚠️ '{dir_path}' não é um diretório. Ignorando...")
        else:
            print(f"ℹ️ Diretório não encontrado: {dir_path}")


def move_files():
    """Move arquivos para os locais corretos"""
    print("\n📂 Movendo arquivos para os diretórios corretos...")

    for filename, dest_path in FILES_TO_MOVE.items():
        src_path = os.path.join(BASE_DIR, filename)
        dest_file_path = os.path.join(dest_path, filename)

        if os.path.exists(src_path):
            os.makedirs(dest_path, exist_ok=True)
            shutil.move(src_path, dest_file_path)
            print(f"📄 Arquivo movido: {src_path} → {dest_file_path}")


def setup_project():
    """Cria a estrutura de diretórios, move arquivos e limpa o projeto"""
    print(f"📂 Organizando projeto em: {BASE_DIR}")

    # Criar os diretórios corretamente
    for directory, sub_dirs in DIR_STRUCTURE.items():
        dir_path = os.path.join(BASE_DIR, directory)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"📁 Diretório criado: {dir_path}")
        else:
            print(f"⚠️ Diretório já existe: {dir_path}")

        for sub_dir in sub_dirs:
            sub_dir_path = os.path.join(dir_path, sub_dir)
            if not os.path.exists(sub_dir_path):
                os.makedirs(sub_dir_path, exist_ok=True)
                print(f"📂 Subdiretório criado: {sub_dir_path}")

    # Criar arquivos essenciais se não existirem
    print("\n📄 Criando arquivos essenciais...")
    for filename, content in FILES.items():
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w") as file:
                file.write(content)
            print(f"✅ Arquivo criado: {filepath}")
        else:
            print(f"⚠️ Arquivo já existe: {filepath}")

    # Remover diretórios desnecessários
    remove_unnecessary_dirs()

    # Mover arquivos existentes para seus locais corretos
    move_files()

    print("\n✅ Projeto organizado com sucesso!")


if __name__ == "__main__":
    setup_project()
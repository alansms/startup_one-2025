import os
import subprocess
import sys

# Caminho base do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Estrutura esperada
EXPECTED_DIRS = [
    "anomaly-detection/esp32",
    "anomaly-detection/sensor-monitoring/data",
    "anomaly-detection/models",
    "anomaly-detection/tests",
]

EXPECTED_FILES = {
    os.path.join(BASE_DIR, "anomaly-detection/requirements.txt"): [
        "fastapi", "uvicorn", "numpy", "scipy", "requests", "pytest", "pydantic", "scikit-learn", "matplotlib", "seaborn"
    ],
    os.path.join(BASE_DIR, "README.md"): [
        "# 📌 Sistema de Monitoramento e Análise Preditiva para Manutenção Industrial"
    ]
}


def ensure_directories():
    for dir_rel in EXPECTED_DIRS:
        dir_path = os.path.join(BASE_DIR, dir_rel)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"📁 Criado: {dir_path}")
        else:
            print(f"✅ Diretório OK: {dir_path}")


def fix_requirements():
    for req_path in EXPECTED_FILES:
        if "requirements.txt" in req_path:
            required = set(EXPECTED_FILES[req_path])
            if os.path.exists(req_path):
                with open(req_path, "r") as file:
                    existing = set([line.strip() for line in file.readlines() if line.strip()])
            else:
                existing = set()

            missing = required - existing
            if missing:
                with open(req_path, "a") as file:
                    for item in missing:
                        file.write(f"{item}\n")
                print(f"🛠️ Atualizado: {req_path}")
            else:
                print(f"✅ requirements.txt já contém todos os pacotes necessários.")


def fix_readme():
    readme_path = os.path.join(BASE_DIR, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as file:
            file.write(EXPECTED_FILES[readme_path][0])
        print(f"📄 Criado: {readme_path}")
    else:
        print("✅ README.md já existe.")


def install_packages():
    print("📦 Instalando pacotes do requirements.txt...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "-r", os.path.join(BASE_DIR, "anomaly-detection/requirements.txt")
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Erro durante a instalação dos pacotes:")
        print(e)


if __name__ == "__main__":
    print("🔧 Iniciando correções no projeto...")
    ensure_directories()
    fix_readme()
    fix_requirements()
    install_packages()
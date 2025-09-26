import os
from pydantic import BaseModel
from pathlib import Path

# Obtém o caminho do diretório raiz do projeto
# O 'Path(__file__).resolve()' garante que estamos na pasta 'core'
# e 'parents[3]' sobe 3 níveis para chegar na raiz do projeto 'car-prediction-api'
ROOT_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseModel):
    # Diretório para logs
    LOG_DIR: Path = ROOT_DIR / "data" / "logs"

    # Caminho para backbone MobileNet
    BACKBONW_PATH: Path = ROOT_DIR / "app" / "models" / "mobilenet_backbone_.pkl"
    
    # Caminho do modelo MLP
    MLP_MODEL_PATH: Path = ROOT_DIR / "app" / "models" / "mlp_model.pkl"
    
    # Caminho do Label Encoder
    LABEL_ENCODER_PATH: Path = ROOT_DIR / "app" / "models" / "mlp_label.pkl"

    # Caminho do modelo SVM
    SVM_MODEL_PATH: Path = ROOT_DIR / "app" / "models" / "svm_model.pkl"
    
    # Caminho do modelo Random Forest
    RANDOM_FOREST_MODEL_PATH: Path = ROOT_DIR / "app" / "models" / "random_forest_model.pkl"
    
    # URL do Redis (exemplo de variável de ambiente)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

# Cria a instância das configurações
settings = Settings()

# Garante que os diretórios necessários existam
# Note que só criamos diretórios, não arquivos
os.makedirs(settings.LOG_DIR, exist_ok=True)

# Diretório do reddis para queue
# REDIS_URL = "redis://localhost:6379"  # URL do Redis

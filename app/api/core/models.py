import joblib
from torchvision import models, transforms

from .config import settings

# Carregar modelo treinado
model = joblib.load(settings.MLP_MODEL_PATH)
encoder = joblib.load(settings.LABEL_ENCODER_PATH)

# Carregar backbone (MobileNet)
backbone = models.mobilenet_v2(weights="DEFAULT").features
backbone.eval()

# Transformação padrão de imagem (redimensiona para 224x224 e normaliza)
image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

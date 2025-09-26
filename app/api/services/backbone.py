from PIL import Image
import io
import torch
import torch.nn as nn
import torchvision.transforms as transforms

def get_vector_from_bytes(backbone, image_bytes: bytes, device: str = 'cuda'):
    """
    Recebe bytes de uma imagem (ex: UploadFile.file.read()),
    processa e retorna o vetor do backbone (MobileNet -> 1280 features).
    """
    try:
        # Converte os bytes em uma imagem PIL RGB
        image_pil = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        # Transformações padrão do ImageNet para MobileNet
        transform = transforms.Compose([
            transforms.Resize((224, 224)),  # mantém formato fixo
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

        # Converte para tensor e envia para o device
        image_tensor = transform(image_pil).unsqueeze(0).to(device)

        # Global Average Pooling para achatar a saída
        global_pool = nn.AdaptiveAvgPool2d((1, 1))
        with torch.no_grad():
            output = backbone(image_tensor)   # (1, 1280, 7, 7)
            pooled = global_pool(output)      # (1, 1280, 1, 1)
            vector = pooled.squeeze().cpu().numpy()  # (1280,)

        return vector

    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None

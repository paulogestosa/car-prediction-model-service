# api/routers/models.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import Annotated
import torch
from PIL import Image
import io
import torch.nn as nn

from ..core.models import model, encoder, backbone, image_transform
from ..services.prediction import predict_with_mlp

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/predict/{model_id}")
async def predict_model(
    model_id: int,
    image: Annotated[UploadFile, File()],
    request: Request   # para acessar o logger
):
    try:
        # Carregar imagem em memória
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Transformar imagem
        input_tensor = image_transform(pil_image).unsqueeze(0)

        # Extrair features com a backbone
        with torch.no_grad():
            output = backbone(input_tensor)          # (1, 1280, 7, 7)
            pooled = nn.AdaptiveAvgPool2d((1, 1))(output)  # (1, 1280, 1, 1)
            features = pooled.view(pooled.size(0), -1).cpu().numpy()  # (1, 1280)

        # Fazer predição
        if model_id == 1:
            prediction = predict_with_mlp(model, encoder, features)

        # Loga a previsão
        if hasattr(request.state, "logger"):
            request.state.logger.log_event("Prediction", {"result": prediction.tolist()})

        return {"model_id": model_id, "prediction": prediction.tolist()}

    except Exception as e:
        if hasattr(request.state, "logger"):
            request.state.logger.log_event("Prediction Error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

"""@router.get("/models/")
async def get_models():
    # Se usasse banco de dados poderíamos retornar todos presentes no banco
    # Como estamos localmente procuramos todos os app/models/... presentes
    return

@router.post("/models/train/")
async def train_models(dataset_x, dataset_y):
    # treina todos os modelos que temos, todos em sequencia dada uma fila, retorna quando terminar de treinar
    return

@router.post("models/train/{id}")
async def train_model(dataset_x, dataset_y, id: int):
    # Treina um modelo específico pelo id dele, só retorna quando terminar de treinar
    return

@router.post("models/predict/")
async def predict_models(image):
    # recebe uma imagem como entrada e retorna a predição dela, de todos os modelos em conjunto
    return"""

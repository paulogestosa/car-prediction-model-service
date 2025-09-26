# Expor funções públicas dos submódulos para import simples:
from .prediction import load_model_and_encoder, predict_with_mlp
from .backbone import get_vector_from_bytes

__all__ = ["load_model_and_encoder", "predict_with_mlp", "load_backbone", "get_vector_from_bytes"]

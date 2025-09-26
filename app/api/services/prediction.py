# api/services/prediction.py
import joblib
import numpy as np

def load_model_and_encoder(model_path: str, label_encoder_path: str):
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)
    return model, label_encoder

def predict_with_mlp(mlp_model, label_encoder, image_features: np.ndarray):
    prediction_encoded = mlp_model.predict(image_features)
    prediction_class = label_encoder.inverse_transform(prediction_encoded)
    return prediction_class

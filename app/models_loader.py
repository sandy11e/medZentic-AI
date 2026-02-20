import os
import joblib
import shap
from .config import MODELS_DIR

def load_model(model_name: str):
    path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)

diabetes_model = load_model("diabetes_model.pkl")
heart_model = load_model("heart_model.pkl")
parkinson_model = load_model("parkinson_model.pkl")

try:
    diabetes_explainer = shap.TreeExplainer(diabetes_model)
except:
    diabetes_explainer = None

try:
    heart_explainer = shap.TreeExplainer(heart_model.named_steps["model"])
except:
    heart_explainer = None
import numpy as np
from .models_loader import (
    diabetes_model,
    heart_model,
    parkinson_model,
    diabetes_explainer,
    heart_explainer
)
from .config import DIABETES_FEATURES, HEART_FEATURES, PARKINSON_FEATURES


def safe_feature_vector(values, feature_list):
    return np.array([[
        float(values.get(f, 0)) for f in feature_list
    ]])


def predict(disease, values):

    if disease == "diabetes":
        model = diabetes_model
        features = DIABETES_FEATURES
        explainer = diabetes_explainer

    elif disease == "heart":
        model = heart_model
        features = HEART_FEATURES
        explainer = heart_explainer

    elif disease == "parkinson":
        model = parkinson_model
        features = PARKINSON_FEATURES
        explainer = None

    else:
        raise ValueError("Unsupported disease")

    feature_array = safe_feature_vector(values, features)

    prediction = model.predict(feature_array)[0]

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(feature_array)[0][1]
    else:
        probability = float(prediction)

    shap_data = []

    if explainer:
        try:
            shap_values = explainer(feature_array)
            vals = shap_values.values[0]
            importance = sorted(zip(features, vals), key=lambda x: abs(x[1]), reverse=True)
            shap_data = [
                {"feature": f, "impact": round(float(v), 4)}
                for f, v in importance[:5]
            ]
        except:
            shap_data = []

    return prediction, probability, shap_data
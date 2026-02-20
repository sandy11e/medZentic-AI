from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load models
diabetes_model = joblib.load("models/diabetes_model.pkl")
heart_model = joblib.load("models/heart_model.pkl")
parkinson_model = joblib.load("models/parkinson_model.pkl")


class PredictionRequest(BaseModel):
    disease: str
    features: dict


@app.post("/predict")
def predict(data: PredictionRequest):

    disease = data.disease.lower()
    features = np.array([list(data.features.values())])

    if disease == "diabetes":
        model = diabetes_model
    elif disease == "heart":
        model = heart_model
    elif disease == "parkinson":
        model = parkinson_model
    else:
        return {"error": "Invalid disease type"}

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    # Convert to readable format
    risk_label = "High Risk" if prediction == 1 else "Low Risk"

    if probability > 0.80:
        confidence = "High"
    elif probability > 0.60:
        confidence = "Moderate"
    else:
        confidence = "Low"

    return {
        "disease": disease,
        "prediction": risk_label,
        "risk_probability": round(float(probability), 2),
        "confidence_level": confidence,
        "analysis_summary": generate_summary(disease, prediction, probability)
    }


def generate_summary(disease, prediction, probability):

    if prediction == 0:
        return f"No strong indicators of {disease} detected."

    if disease == "diabetes":
        return "Elevated glucose and insulin-related markers detected."

    if disease == "heart":
        return "Cardiac stress indicators and cholesterol patterns suggest risk."

    if disease == "parkinson":
        return "Voice frequency instability and tremor-related acoustic patterns detected."

    return "Risk factors identified."
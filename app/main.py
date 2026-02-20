from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
from typing import Dict, Any, List

from .config import UPLOAD_DIR
from .database import init_db, save_prediction
from .prediction_engine import predict
from .analysis_engine import build_analysis
from .llm_engine import query_llm
from .extraction import (
    extract_text,
    extract_all_parameters,
    extract_parkinson
)

app = FastAPI(title="MedZentic AI Backend")

os.makedirs(UPLOAD_DIR, exist_ok=True)
init_db()

# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():
    return {"status": "running"}


# =====================================================
# MANUAL PREDICTION
# =====================================================

class PredictionRequest(BaseModel):
    disease: str
    features: dict


@app.post("/predict")
def manual_predict(data: PredictionRequest):

    prediction, probability, shap_data = predict(
        data.disease,
        data.features
    )

    analysis, risk_label = build_analysis(
        data.disease,
        prediction,
        probability,
        shap_data,
        data.features
    )

    prediction_id = save_prediction(
        data.disease,
        probability,
        risk_label,
        None,
        analysis
    )

    analysis["prediction_id"] = prediction_id

    return analysis


# =====================================================
# REPORT ANALYSIS
# =====================================================

@app.post("/analyze-report")
def analyze_report(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    extracted_values = extract_all_parameters(text)

    results = {}

    # -----------------------
    # Diabetes
    # -----------------------

    diabetes_required = ["Glucose", "BMI", "BloodPressure", "Age"]

    if all(feature in extracted_values for feature in diabetes_required):

        prediction, probability, shap_data = predict(
            "diabetes",
            extracted_values
        )

        analysis, risk_label = build_analysis(
            "diabetes",
            prediction,
            probability,
            shap_data,
            extracted_values
        )

        results["diabetes"] = analysis

    else:
        results["diabetes"] = {
            "status": "Insufficient data for diabetes evaluation"
        }

    # -----------------------
    # Heart
    # -----------------------

    heart_required = ["Cholesterol", "trestbps", "Age"]

    if all(feature in extracted_values for feature in heart_required):

        prediction, probability, shap_data = predict(
            "heart",
            extracted_values
        )

        analysis, risk_label = build_analysis(
            "heart",
            prediction,
            probability,
            shap_data,
            extracted_values
        )

        results["heart"] = analysis

    else:
        results["heart"] = {
            "status": "Insufficient data for heart disease evaluation"
        }

    # -----------------------
    # Parkinson
    # -----------------------

    parkinson_values = extract_parkinson(text)

    if len(parkinson_values) >= 3:

        prediction, probability, shap_data = predict(
            "parkinson",
            parkinson_values
        )

        analysis, risk_label = build_analysis(
            "parkinson",
            prediction,
            probability,
            shap_data,
            parkinson_values
        )

        results["parkinson"] = analysis

    else:
        results["parkinson"] = {
            "status": "Insufficient neurological acoustic parameters for Parkinson evaluation."
        }

    return {
        "extracted_values": extracted_values,
        "results": results
    }


# =====================================================
# CHAT
# =====================================================

class ChatRequest(BaseModel):
    question: str
    analysis: Dict[str, Any]
    history: List[Dict[str, str]] = []


@app.post("/chat")
def chat(data: ChatRequest):

    answer = query_llm(
        data.analysis,
        data.question,
        data.history
    )

    return {
        "answer": answer
    }


# =====================================================
# ANALYTICS
# =====================================================

@app.get("/analytics")
def analytics():

    from .config import DATABASE_PATH
    import sqlite3

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_label='High Risk'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT disease, COUNT(*) FROM predictions GROUP BY disease")
    disease_counts = cursor.fetchall()

    conn.close()

    return {
        "total_predictions": total,
        "high_risk_cases": high,
        "high_risk_percentage": round((high / total) * 100, 2) if total else 0,
        "disease_distribution": {d[0]: d[1] for d in disease_counts}
    }
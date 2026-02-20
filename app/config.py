import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODELS_DIR = os.path.join(BASE_DIR, "models")
DATABASE_PATH = os.path.join(BASE_DIR, "medzentic.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

DIABETES_FEATURES = [
    "Pregnancies", "Glucose", "BloodPressure",
    "SkinThickness", "Insulin", "BMI",
    "DiabetesPedigreeFunction", "Age"
]

HEART_FEATURES = [
    "age","sex","cp","trestbps","chol","fbs",
    "restecg","thalach","exang","oldpeak",
    "slope","ca","thal"
]
PARKINSON_FEATURES = [
    "MDVP:Fo(Hz)",
    "MDVP:Fhi(Hz)",
    "MDVP:Flo(Hz)",
    "MDVP:Jitter(%)",
    "MDVP:Shimmer",
    "HNR"
]
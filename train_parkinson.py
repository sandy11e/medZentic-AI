import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("data/parkinson.csv")

selected_features = [
    "PPE",
    "DFA",
    "RPDE",
    "locPctJitter",
    "locShimmer",
    "meanNoiseToHarmHarmonicity"
]

X = df[selected_features]
y = df["class"]

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipeline.fit(X_train, y_train)

print("Accuracy:", accuracy_score(y_test, pipeline.predict(X_test)))

joblib.dump(pipeline, "models/parkinson_model.pkl")

print("Lightweight Parkinson model saved.")
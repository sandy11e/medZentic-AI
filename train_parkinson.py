import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

# Load dataset
df = pd.read_csv("data/parkinson.csv")

# Drop name column if present
if "name" in df.columns:
    df = df.drop("name", axis=1)

X = df.drop("class", axis=1)
y = df["class"]

# Create pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=300,
        random_state=42
    ))
])

# Cross validation
cv_scores = cross_val_score(pipeline, X, y, cv=5)

print("Cross Validation Accuracy:", np.mean(cv_scores))

# Train final model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipeline.fit(X_train, y_train)

pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print("Final Test Accuracy:", accuracy)

# Save model
joblib.dump(pipeline, "models/parkinson_model.pkl")

print("Parkinson model saved successfully.")
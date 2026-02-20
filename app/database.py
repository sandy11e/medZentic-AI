import sqlite3
import json
from datetime import datetime
from .config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease TEXT,
        risk_label TEXT,
        probability REAL,
        confidence TEXT,
        analysis_json TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_prediction(disease, probability, risk_label, confidence, analysis_json):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions (disease, risk_label, probability, confidence, analysis_json, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        disease,
        risk_label,
        probability,
        "",
        json.dumps(analysis_json),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prediction_id

def get_prediction(prediction_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT analysis_json FROM predictions WHERE id=?", (prediction_id,))
    row = cursor.fetchone()
    conn.close()

    return json.loads(row[0]) if row else None
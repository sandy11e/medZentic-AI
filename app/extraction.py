import pdfplumber
import re


def extract_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text


def regex_extract(text, patterns):
    values = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                values[key] = float(match.group(1))
            except:
                pass
    return values


def extract_all_parameters(text):

    patterns = {
        # Diabetes related
        "Glucose": r"Glucose.*?(\d+\.?\d*)",
        "BMI": r"BMI.*?(\d+\.?\d*)",
        "BloodPressure": r"Blood\s*Pressure.*?(\d+\.?\d*)",
        "Insulin": r"Insulin.*?(\d+\.?\d*)",
        "Pregnancies": r"Pregnancies.*?(\d+)",
        "DiabetesPedigreeFunction": r"DiabetesPedigreeFunction.*?(\d+\.?\d*)",
        "Age": r"Age.*?(\d+)",

        # Heart related
        "Cholesterol": r"Cholesterol.*?(\d+\.?\d*)",
        "thalach": r"Heart\s*Rate.*?(\d+\.?\d*)",
        "trestbps": r"Blood\s*Pressure.*?(\d+\.?\d*)",
    }

    return regex_extract(text, patterns)

def extract_parkinson(text):
    return regex_extract(text, {
        "MDVP:Fo(Hz)": r"Fo\(Hz\)\s*[:\-]?\s*(\d+\.?\d*)",
        "MDVP:Fhi(Hz)": r"Fhi\(Hz\)\s*[:\-]?\s*(\d+\.?\d*)",
        "MDVP:Flo(Hz)": r"Flo\(Hz\)\s*[:\-]?\s*(\d+\.?\d*)",
        "MDVP:Jitter(%)": r"Jitter\s*[:\-]?\s*(\d+\.?\d*)",
        "MDVP:Shimmer": r"Shimmer\s*[:\-]?\s*(\d+\.?\d*)",
        "HNR": r"HNR\s*[:\-]?\s*(\d+\.?\d*)"
    })
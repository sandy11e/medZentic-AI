def build_analysis(disease, prediction, probability, shap_data, values):

    risk_label = "High Risk" if prediction == 1 else "Low Risk"

    interpreted_values = interpret_values(disease, values)

    explanation = generate_simple_explanation(disease, risk_label, interpreted_values)

    analysis = {
        "summary": {
            "condition": disease,
            "risk_level": risk_label,
            "risk_probability": round(float(probability), 2)
        },
        "health_parameters": interpreted_values,
        "doctor_explanation": explanation
    }

    return analysis, risk_label


def interpret_values(disease, values):

    normal_ranges = {
        "Glucose": (70, 140),
        "BMI": (18.5, 24.9),
        "BloodPressure": (80, 120),
        "Cholesterol": (125, 200),
        "Age": (0, 120)
    }

    interpreted = []

    for key, value in values.items():

        status = "Normal"

        if key in normal_ranges:
            low, high = normal_ranges[key]
            if value < low:
                status = "Below Normal"
            elif value > high:
                status = "Above Normal"

        interpreted.append({
            "parameter": key,
            "value": value,
            "status": status
        })

    return interpreted


def generate_simple_explanation(disease, risk_label, interpreted_values):

    high_factors = [
        item["parameter"]
        for item in interpreted_values
        if item["status"] == "Above Normal"
    ]

    if risk_label == "Low Risk":
        return "Your health indicators are mostly within normal ranges. Current risk appears low."

    if high_factors:
        return f"Your {', '.join(high_factors)} values are higher than normal, which increases the likelihood of {disease}."

    return f"Some health indicators suggest possible {disease}. Further medical consultation is recommended."
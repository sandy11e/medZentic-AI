import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"


def is_analysis_question(question: str) -> bool:
    keywords = [
        "risk", "probability", "confidence",
        "prediction", "analysis", "result",
        "glucose", "cholesterol", "bmi",
        "heart", "diabetes", "value"
    ]

    question = question.lower()
    return any(word in question for word in keywords)


def query_llm(context_data, question, chat_history=None):

    if chat_history is None:
        chat_history = []

    # Build conversation history
    history_text = ""
    for item in chat_history:
        history_text += f"User: {item['user']}\nAssistant: {item['assistant']}\n"

    if is_analysis_question(question):
        system_prompt = f"""
You are a medical AI assistant.

If the question relates to medical analysis,
you MUST answer strictly from the structured analysis below.
Do NOT invent values.

STRUCTURED DATA:
{json.dumps(context_data, indent=2)}

Conversation so far:
{history_text}

User: {question}
Assistant:
"""
    else:
        system_prompt = f"""
You are a helpful, intelligent AI assistant.
Respond naturally and conversationally.

Conversation so far:
{history_text}

User: {question}
Assistant:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": system_prompt,
                "stream": False
            },
            timeout=60
        )

        return response.json().get("response", "No response.")

    except:
        return "LLM service unavailable."
import os
import requests
import google.generativeai as genai

# =========================
# 🔧 CONFIG
# =========================

LLM_PROVIDER = "gemini"  
# values: "gemini" or "ollama"

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# Ollama setup
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


# =========================
# 🚀 MAIN FUNCTION
# =========================

def generate_response(prompt: str) -> str:
    if LLM_PROVIDER == "gemini":
        return generate_gemini_response(prompt)
    elif LLM_PROVIDER == "ollama":
        return generate_ollama_response(prompt)
    else:
        return "Error: Invalid LLM provider"


# =========================
# 🤖 GEMINI
# =========================

def generate_gemini_response(prompt: str) -> str:
    try:
        response = gemini_model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "No response from Gemini"

    except Exception as e:
        return f"Gemini Error: {str(e)}"


# =========================
# 🦙 OLLAMA (LOCAL LLM)
# =========================

def generate_ollama_response(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            return f"Ollama Error: {response.text}"

        data = response.json()

        return data.get("response", "").strip()

    except Exception as e:
        return f"Ollama Error: {str(e)}"
import os
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY", "").strip()

if not api_key:
    raise ValueError("GEMINI_API_KEY não configurada")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

@app.get("/")
def home():
    return {"status": "Psico-Tech Online", "mensagem": "Sistema operando"}

@app.get("/gerar")
def gerar(pergunta: str):
    try:
        response = model.generate_content(pergunta)
        return {"resposta": response.text}
    except Exception as e:
        return {"erro": str(e)}

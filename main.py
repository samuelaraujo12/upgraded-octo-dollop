import os
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# Puxa a chave GOOGLE_API_KEY que configuramos na Render
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Modelo configurado corretamente
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def home():
    return {"status": "Psico-Tech App Online"}

@app.get("/gerar")
def gerar(pergunta: str):
    try:
        response = model.generate_content(pergunta)
        return {"resposta": response.text}
    except Exception as e:
        return {"erro": str(e)}

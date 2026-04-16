import os
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# A chave deve estar em uma linha só, entre aspas
api_key = "AIzaSyBBiYcME8FJ9ROzJJ-1f-1DH8r23yRMp08"

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def home():
    return {"status": "Psico-Tech App Online", "mensagem": "Servidor rodando com sucesso!"}

@app.get("/gerar")
def gerar(pergunta: str):
    try:
        response = model.generate_content(pergunta)
        return {"resposta": response.text}
    except Exception as e:
        return {"erro": str(e)}

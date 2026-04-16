import os
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# COLE SUA CHAVE ENTRE AS ASPAS ABAIXO (A que começa com AIza...)
api_key = "COLE_SUA_CHAVE_AQUI" 

genai.configure(api_key=api_key)

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

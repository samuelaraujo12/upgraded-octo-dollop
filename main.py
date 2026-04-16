import os
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# Substitua o texto abaixo pela sua chave que começa com AIza
# Mantenha as aspas! Exemplo: api_key = "AIzaSy..."
api_key = "COLE_AQUI_SUA_CHAVE_AIZA"

genai.configure(api_key=api_key)

# Configuração do modelo Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def home():
    return {"status": "Psico-Tech App Online", "mensagem": "Servidor rodando com sucesso!"}

@app.get("/gerar")
def gerar(pergunta: str):
    try:
        # Chama a IA para responder
        response = model.generate_content(pergunta)
        return {"resposta": response.text}
    except Exception as e:
        # Se der erro (como chave inválida), ele avisa aqui
        return {"erro": str(e)}

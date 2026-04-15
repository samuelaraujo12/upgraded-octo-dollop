from fastapi import FastAPI
import google.generativeai as genai
import os

app = FastAPI()

# Configura a IA com a chave da Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Online", "projeto": "Tecnologia e Psicologia"}

@app.get("/gerar")
def gerar(pergunta: str):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(pergunta)
    return {"resposta": response.text}

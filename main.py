
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from openai import OpenAI

app = FastAPI()

API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

@app.get("/")
@app.head("/")
def home():
    return {"status": "online", "mensagem": "Psico-Tech rodando"}

@app.get("/gerar")
@app.head("/gerar")
def gerar(pergunta: str = "ping"):
    try:
        if not API_KEY:
            return {"erro": "OPENROUTER_API_KEY não configurada na Render"}

        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            extra_headers={
                "HTTP-Referer": "https://psico-tech-app.onrender.com",
                "X-Title": "Psico-Tech IA"
            },
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em psicologia e tecnologia. Responda de forma clara e objetiva."},
                {"role": "user", "content": pergunta},
            ],
        )

        return {"resposta": completion.choices[0].message.content}

    except Exception as e:
        return {"erro": str(e)}

@app.get("/ui")
@app.head("/ui")
def ui():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(file_path)

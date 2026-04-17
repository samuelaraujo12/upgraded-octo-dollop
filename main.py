
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@app.get("/")
@app.head("/")
def home():
    return {"status": "online", "mensagem": "Psico-Tech rodando"}

@app.get("/gerar")
@app.head("/gerar")
def gerar(pergunta: str = "ping"):
    try:
        completion = client.chat.completions.create(
            model="google/gemma-4-26b-a4b-it:free",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em psicologia e tecnologia."},
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

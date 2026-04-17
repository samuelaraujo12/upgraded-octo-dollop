import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from openai import OpenAI

app = FastAPI()

# OpenRouter API (CORRETO)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@app.get("/")
def home():
    return {"status": "online", "mensagem": "Psico-Tech rodando"}

@app.get("/gerar")
def gerar(pergunta: str):
    try:
        completion = client.chat.completions.create(
            model="google/gemma-4-26b-a4b-it:free",
            messages=[
                {"role": "user", "content": pergunta}
            ],
        )

        return {"resposta": completion.choices[0].message.content}

    except Exception as e:
        return {"erro": str(e)}

# 👉 INTERFACE VISUAL
@app.get("/ui")
def ui():
    return FileResponse("index.html")

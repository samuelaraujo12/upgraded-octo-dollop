import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

if not HF_TOKEN:
    raise ValueError("HF_TOKEN não configurado")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

@app.get("/")
def home():
    return {"status": "Psico-Tech Online", "mensagem": "Rodando com Hugging Face"}

@app.get("/gerar")
def gerar(pergunta: str):
    try:
        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=[
                {"role": "system", "content": "Você é especialista em psicologia e tecnologia."},
                {"role": "user", "content": pergunta},
            ],
        )

        return {"resposta": completion.choices[0].message.content}

    except Exception as e:
        return {"erro": str(e)}

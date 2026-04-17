import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("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"),
)

@app.get("/")
def home():
    return {"status": "online"}

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

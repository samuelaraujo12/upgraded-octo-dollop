import os
import logging
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# =========================
# LOGGING (Modo Avançado)
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("psico-tech-app")

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Psico-Tech API",
    version="1.0",
    description="API de IA focada em Psicologia e Tecnologia usando OpenRouter"
)

# =========================
# CORS (Para aceitar frontend, sites, etc.)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção pode restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# OPENROUTER CONFIG
# =========================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    logger.warning("⚠️ OPENROUTER_API_KEY não foi encontrada no ambiente!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# =========================
# ROTAS
# =========================

@app.get("/")
@app.head("/")
def home():
    return {"status": "online", "mensagem": "Psico-Tech rodando com sucesso"}


@app.get("/gerar")
@app.head("/gerar")
def gerar(
    pergunta: str = Query(default="ping", min_length=1, max_length=500)
):
    if not OPENROUTER_API_KEY:
        return JSONResponse(
            status_code=500,
            content={"erro": "OPENROUTER_API_KEY não configurada no Render"}
        )

    try:
        logger.info(f"📩 Pergunta recebida: {pergunta}")

        completion = client.chat.completions.create(
            model="google/gemma-2-9b-it:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente especializado em psicologia e tecnologia. "
                        "Responda com clareza, didática e exemplos práticos. "
                        "Evite respostas longas demais, seja objetivo."
                    )
                },
                {"role": "user", "content": pergunta},
            ],
        )

        resposta = completion.choices[0].message.content

        logger.info("✅ Resposta gerada com sucesso")

        return {
            "status": "ok",
            "pergunta": pergunta,
            "resposta": resposta
        }

    except Exception as e:
        logger.error(f"❌ Erro ao chamar OpenRouter: {str(e)}")

        return JSONResponse(
            status_code=500,
            content={
                "status": "erro",
                "mensagem": "Falha ao gerar resposta da IA",
                "detalhes": str(e)
            }
        )


@app.get("/ui")
@app.head("/ui")
def ui():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")

    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={"erro": "Arquivo index.html não encontrado"}
        )

    return FileResponse(file_path)

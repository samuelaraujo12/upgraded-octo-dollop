import os
import time
import logging
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# =========================
# LOGGING (Avançado)
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("psico-tech-app")

# =========================
# APP
# =========================
app = FastAPI(
    title="Psico-Tech API",
    version="2.0",
    description="API IA Psicologia + Tecnologia usando OpenRouter"
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# OPENROUTER CONFIG
# =========================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    logger.warning("⚠️ OPENROUTER_API_KEY NÃO CONFIGURADA!")

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
    return {"status": "online", "mensagem": "Psico-Tech rodando"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "openrouter_key": bool(OPENROUTER_API_KEY)
    }


@app.get("/gerar")
@app.head("/gerar")
def gerar(pergunta: str = Query(default="ping", min_length=1, max_length=800)):

    if not OPENROUTER_API_KEY:
        return JSONResponse(
            status_code=500,
            content={
                "status": "erro",
                "mensagem": "OPENROUTER_API_KEY não configurada no Render (Environment Variables)."
            }
        )

    tentativas = 3
    ultima_erro = None

    for tentativa in range(1, tentativas + 1):
        try:
            logger.info(f"📩 Pergunta recebida: {pergunta}")
            logger.info(f"🔁 Tentativa {tentativa}/{tentativas}")

            start_time = time.time()

            completion = client.chat.completions.create(
                model="google/gemma-2-9b-it:free",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um assistente especializado em psicologia e tecnologia. "
                            "Responda de forma clara, organizada e prática. "
                            "Se possível, dê exemplos."
                        )
                    },
                    {"role": "user", "content": pergunta},
                ],
            )

            tempo_total = round(time.time() - start_time, 2)

            resposta = completion.choices[0].message.content

            logger.info(f"✅ Resposta gerada com sucesso em {tempo_total}s")

            return {
                "status": "ok",
                "tempo_resposta": f"{tempo_total}s",
                "pergunta": pergunta,
                "resposta": resposta
            }

        except Exception as e:
            ultima_erro = str(e)
            logger.error(f"❌ Erro na tentativa {tentativa}: {ultima_erro}")

            # Espera antes de tentar de novo
            time.sleep(1.5)

    return JSONResponse(
        status_code=500,
        content={
            "status": "erro",
            "mensagem": "Falha ao gerar resposta da IA após 3 tentativas",
            "detalhes": ultima_erro
        }
    )


@app.get("/ui")
@app.head("/ui")
def ui():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")

    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=404,
            content={"erro": "index.html não encontrado no projeto"}
        )

    return FileResponse(file_path)

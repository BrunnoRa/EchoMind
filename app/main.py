from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1 import auth, faq, documents, voice, metrics, unanswered
import os

app = FastAPI(title="Totem Universitário API")

# --- CONFIGURAÇÃO DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# --- ROTAS ---
app.include_router(auth.router, prefix="/api/v1")
app.include_router(faq.router, prefix="/api/v1")
# app.include_router(events.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(voice.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")
app.include_router(unanswered.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        from sqlalchemy import text
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
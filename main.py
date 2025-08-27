from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import nanoid
import os
from database import supabase
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
    # "https://seu-frontend.vercel.app",
]

class URLBase(BaseModel):
    original_url: HttpUrl

app = FastAPI(title="API Encurtador de URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Encurtador de URL!"}

@app.post("/encurtar", status_code=201)
def encurtar_url(url: URLBase):
    short_code = nanoid.generate(size=7) # Gera um código de 7 caracteres

    try:
        # Insere no banco de dados
        data, count = supabase.table('urls').insert({
            "original_url": str(url.original_url),
            "short_code": short_code
        }).execute()

    except Exception as e:
        # Em caso de erro no banco de dados
        raise HTTPException(status_code=500, detail="Erro ao se comunicar com o banco de dados.")

    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    short_url = f"{base_url}/{short_code}"

    return {"short_url": short_url}

@app.get("/{short_code}")
def redirecionar(short_code: str):
    try:
        # Busca pelo código no banco de dados
        data, count = supabase.table('urls').select('original_url').eq('short_code', short_code).execute()

        # Verifica se encontrou algum registro
        if not data[1]: # data[1] contém a lista de resultados
            raise HTTPException(status_code=404, detail="URL não encontrada.")

        original_url = data[1][0]['original_url']

        # Retorna uma resposta de redirecionamento
        return RedirectResponse(url=original_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")

from fastapi import FastAPI

app = FastAPI(title="API Encurtador de URL")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Encurtador de URL!"}

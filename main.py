from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Servidor ZapWork webhook ativo."}

@app.post("/webhook")
async def receive_webhook(request: Request, authorization: str = Header(None)):
    if authorization != API_KEY:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    try:
        data = await request.json()
        # Aqui você pode processar os dados recebidos do ZapWork
        print("📩 Webhook recebido:", data)

        return {"status": "success", "message": "Webhook processado"}
    except Exception as e:
        print("❌ Erro ao processar webhook:", e)
        return JSONResponse(status_code=400, content={"error": "Invalid request"})

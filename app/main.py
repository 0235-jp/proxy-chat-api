from fastapi import FastAPI, Request
from api import get_all_models, get_chat_completions

app = FastAPI()

@app.get("/v1/models")
async def models(request: Request):
    return await get_all_models(request)

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    return await get_chat_completions(request)

from fastapi import FastAPI, Request
from api import get_models, get_chat_completions

app = FastAPI()

@app.post("/v1/models")
async def models(request: Request):
    return await get_models(request)

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    return await get_chat_completions(request)

import json
from fastapi import HTTPException, Request
from config import SECRET_TOKEN, OPEN_API_KEY, FIREWORKS_API_KEY
import openai

async def get_chat_completions(request: Request):
    signature = request.headers['Authorization']
    if signature != "Bearer " + SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Not authorized")
    body_raw = await request.body()
    body = json.loads(body_raw.decode("utf-8"))
    model = body["model"]
    if model.startswith("accounts/fireworks/models"):
      openai.api_base = "https://api.fireworks.ai/inference/v1/"
      openai.api_key = FIREWORKS_API_KEY
    else:
      openai.api_base = "https://api.openai.com/v1/"
      openai.api_key = OPEN_API_KEY
    response = openai.ChatCompletion.create(model=model, messages=body["messages"])
    return response

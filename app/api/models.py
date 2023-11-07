from fastapi import HTTPException, Request
from config import SECRET_TOKEN, OPEN_API_KEY, FIREWORKS_API_KEY
from openai import AsyncOpenAI

async def get_all_models(request: Request):
    signature = request.headers['Authorization']
    if signature != "Bearer " + SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Not authorized")
    fireworksModels = await get_fireworks_models()
    openaiModels = await get_openai_models()
    return {'data': list(fireworksModels.data + openaiModels.data), "object": "list"}

async def get_models(base_url, api_key):
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    return await client.models.list()

async def get_fireworks_models():
    return await get_models("https://api.fireworks.ai/inference/v1/", FIREWORKS_API_KEY)

async def get_openai_models():
    return await get_models("https://api.openai.com/v1/", OPEN_API_KEY)

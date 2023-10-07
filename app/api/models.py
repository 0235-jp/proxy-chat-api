from fastapi import HTTPException, Request
from config import SECRET_TOKEN, OPEN_API_KEY, FIREWORKS_API_KEY
import openai

async def get_all_models(request: Request):
    signature = request.headers['Authorization']
    if signature != "Bearer " + SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Not authorized")
    fireworksModels = await get_fireworks_models()
    openaiModels = await get_openai_models()
    return list(fireworksModels + openaiModels)

async def get_models(api_base, api_key):
    return openai.Model.list(api_base=api_base, api_key=api_key).data

async def get_fireworks_models():
    return await get_models("https://api.fireworks.ai/inference/v1/", FIREWORKS_API_KEY)

async def get_openai_models():
    return await get_models("https://api.openai.com/v1/", OPEN_API_KEY)

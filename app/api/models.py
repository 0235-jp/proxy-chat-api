import google.generativeai as palm
from fastapi import HTTPException, Request
from config import SECRET_TOKEN, OPEN_API_KEY, FIREWORKS_API_KEY, PALM_KEY
from openai import AsyncOpenAI

palm.configure(api_key=PALM_KEY)

async def get_all_models(request: Request):
    signature = request.headers['Authorization']
    if signature != "Bearer " + SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Not authorized")
    fireworksModels = await get_fireworks_models()
    openaiModels = await get_openai_models()
    googleModels = await get_google_models()
    return {'data': list(fireworksModels + openaiModels + googleModels), "object": "list"}

async def get_models(base_url, api_key):
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    return await client.models.list()

async def get_fireworks_models():
    result =  await get_models("https://api.fireworks.ai/inference/v1/", FIREWORKS_API_KEY)
    models = []
    for model in result.data:
        models.append({
            "id": "fireworks/" + model.id,
            "object": model.object,
            "created": model.created,
             "owned_by": model.owned_by
        })
    return models

async def get_openai_models():
    result = await get_models("https://api.openai.com/v1/", OPEN_API_KEY)
    models = []
    for model in result.data:
        models.append({
            "id": "openai/" + model.id,
            "object": model.object,
            "created": model.created,
             "owned_by": model.owned_by
        })
    return models

async def get_google_models():
    result = palm.list_models()
    models = []
    for model in result:
        models.append({
            "id": "google/" + model.name,
            "object": "model",
            "created": "",
            "owned_by": "google"
        })
    return models
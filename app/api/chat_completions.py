import json
from fastapi import HTTPException, Request
from fastapi.responses import StreamingResponse
from config import SECRET_TOKEN, OPEN_API_KEY, FIREWORKS_API_KEY
import openai
from typing import Iterator

def create(model, body: json):
    create_kwargs = {
        "model": model,
        "messages": body["messages"],
    }
    if "frequency_penalty" in body:
        create_kwargs["frequency_penalty"] = body["frequency_penalty"]
    if "function_call" in body:
        create_kwargs["function_call"] = body["function_call"]
    if "functions" in body:
        create_kwargs["functions"] = body["functions"]
    if "logit_bias" in body:
        create_kwargs["logit_bias"] = body["logit_bias"]
    if "max_tokens" in body:
        create_kwargs["max_tokens"] = body["max_tokens"]
    if "n" in body:
        create_kwargs["n"] = body["n"]
    if "presence_penalty" in body:
        create_kwargs["presence_penalty"] = body["presence_penalty"]
    if "stop" in body:
        create_kwargs["stop"] = body["stop"]
    if "stream" in body:
        create_kwargs["stream"] = body["stream"]
    if "temperature" in body:
        create_kwargs["temperature"] = body["temperature"]
    if "top_p" in body:
        create_kwargs["top_p"] = body["top_p"]
    if "user" in body:
        create_kwargs["user"] = body["user"]
    return openai.ChatCompletion.create(**create_kwargs)

def chat_stream_generator(model, body: json) -> Iterator[bytes]:
   response = create(model, body)
   for chunk in response:
       formatted_chunk = f"data: {json.dumps(chunk)}\n\n"
       yield formatted_chunk

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
    # elif model == "gpt-4":
    #   openai.api_base = "https://api.fireworks.ai/inference/v1/"
    #   openai.api_key = FIREWORKS_API_KEY
    #   model = "accounts/fireworks/models/llama-v2-34b-code-instruct"
    else:
      openai.api_base = "https://api.openai.com/v1/"
      openai.api_key = OPEN_API_KEY
    if body.get("stream", False):
        return StreamingResponse(chat_stream_generator(model, body), media_type="text/event-stream")
    return create(model, body)

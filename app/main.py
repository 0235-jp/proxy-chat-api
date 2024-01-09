import os
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, Header, FastAPI, Request
from memgpt.config import AgentConfig
from memgpt import MemGPT
from memgpt.cli.cli import QuickstartChoice
import deepl
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
    StickerMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    ImagemapMessage,
    TemplateMessage,
    FlexMessage,
)
from linebot.v3.webhooks import (
    MessageEvent,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = MemGPT(
    auto_save=True,
    quickstart=QuickstartChoice.memgpt_hosted,
    config={}
)
agent_config = AgentConfig(
    name=os.getenv("AGENT_NAME"),
    persona=os.getenv("PERSONA_NAME"),
    human=os.getenv("HUMAN_NAME"),
)
agent_id = client.create_agent(agent_config=agent_config)

LINE_BOT_TOKEN = os.getenv("LINE_BOT_TOKEN")
LINE_BOT_SECRET = os.getenv("LINE_BOT_SECRET")
configuration = Configuration(access_token=LINE_BOT_TOKEN)
handler = WebhookHandler(LINE_BOT_SECRET)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)

DEEPL_KEY = os.getenv("DEEPL_KEY")
DEEP_GLOSSARY_KEY = os.getenv("DEEP_GLOSSARY_KEY")
translator = deepl.Translator(DEEPL_KEY)

@app.post("/chat")
async def chat(request: Request):
    body = await request.body()
    signature = request.headers['X-Line-Signature']
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")
    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):
    source = event.source
    replyMessage(source.user_id, event.message.text)

def replyMessage(chatId: str, message: str):
    translateEn = translator.translate_text(message, target_lang="EN-US")
    response = client.user_message(agent_id=agent_id, message=translateEn.text)
    for r in response:
        if "assistant_message" in r:
            my_glossary = translator.get_glossary(DEEP_GLOSSARY_KEY)
            translateJa = translator.translate_text(r["assistant_message"], source_lang="EN", target_lang="JA", glossary=my_glossary)
            line_bot_api.push_message_with_http_info(
                PushMessageRequest(
                    to=chatId,
                    messages=[TextMessage(text=translateJa.text)]
                )
            )
        elif "thoughts" in r:
            translateJa = translator.translate_text(r["internal_monologue"], target_lang="JA")
            line_bot_api.push_message_with_http_info(
                PushMessageRequest(
                    to=chatId,
                    messages=[TextMessage(text=translateJa.text)]
                )
            )

import os
import deepl

SECRET_TOKEN = os.getenv("SECRET_TOKEN")
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
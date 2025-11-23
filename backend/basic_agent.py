from google import genai
from prompts import BASIC_AGENT_PROMPT
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def basic_agent(history):
    text = BASIC_AGENT_PROMPT
    for msg in history:
        text += f"{msg['role']}: {msg['text']}\n"

    res = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=text
    )
    return res.text
# api.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from urllib.parse import quote
from twilio.rest import Client as TwilioClient
from router_agent import AgentRouter
from memory import redis_client
import xml.sax.saxutils as saxutils
import threading
import time
import os

load_dotenv()

app = FastAPI()

app.mount("/product_images", StaticFiles(directory="product_images"), name="product_images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

@app.post("/chat")
async def chat_api(data: ChatRequest):
    return await AgentRouter.run(
        session_id=data.session_id,
        user_message=data.user_message
    )

# -------------------- WHATSAPP ENDPOINT --------------------

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_NUMBER")
PUBLIC_HOST = os.getenv("PUBLIC_HOST")

twilio_client = TwilioClient(TWILIO_SID, TWILIO_AUTH)

def send_products_after_delay(to_number, products):
    time.sleep(1.2)
    for p in products:
        time.sleep(0.6)
        img = quote(p["image_path"])
        media_url = f"https://{PUBLIC_HOST}/product_images/{img}"

        caption = f"{p['name']}\n{p['subtitle']}\nPrice: {p['price']}\n{p['url']}"

        twilio_client.messages.create(
            body=caption,
            media_url=[media_url],
            from_=TWILIO_FROM,
            to=to_number
        )

@app.post("/whatsapp")
async def whatsapp_handler(
    From: str = Form(...),
    Body: str = Form(...)
):
    session_id = From.replace("whatsapp:", "")
    user_message = Body

    result = await AgentRouter.run(session_id, user_message)

    assistant_msg = saxutils.escape(result["assistant_message"])

    xml = f"""
<Response>
    <Message>{assistant_msg}</Message>
</Response>
""".strip()

    if result["products"]:
        threading.Thread(
            target=send_products_after_delay,
            args=(From, result["products"])
        ).start()

    return Response(content=xml, media_type="application/xml")

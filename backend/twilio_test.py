from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

sid = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER")
to_whatsapp = "whatsapp:+919650367672"   # replace with your WhatsApp number

print("Using SID:", sid)
print("Using Token:", token[:6] + "***********")

client = Client(sid, token)

try:
    msg = client.messages.create(
        body="Twilio test message working fine!",
        from_=from_whatsapp,
        to=to_whatsapp
    )
    print("Message sent! SID:", msg.sid)

except Exception as e:
    print("Error:", e)
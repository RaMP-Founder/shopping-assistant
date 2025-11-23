# router_agent.py
from google import genai
from dotenv import load_dotenv
import os
from memory import get_history, append_history
from prompts import MASTER_ROUTER_PROMPT, BASIC_AGENT_PROMPT, get_shopping_prompt
from shopping_agent import rag_search  # ONLY import this

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class AgentRouter:

    @staticmethod
    async def run(session_id: str, user_message: str):
        history = get_history(session_id)

        routing_input = f"History: {history}\nUser: {user_message}"

        route = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[MASTER_ROUTER_PROMPT, routing_input]
        ).text.strip().lower()

        append_history(session_id, "user", user_message)

        if "shopping" in route:
            result = rag_search(session_id, user_message)
            append_history(session_id, "assistant", result["assistant_message"])
            return result

        else:
            reply = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=[BASIC_AGENT_PROMPT, f"User: {user_message}"]
            ).text
            append_history(session_id, "assistant", reply)
            return {
                "assistant_message": reply,
                "products": []
            }
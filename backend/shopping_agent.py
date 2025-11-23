# shopping_agent.py
import numpy as np
import faiss
import pickle
from google import genai
from dotenv import load_dotenv
import os
from memory import get_history
from prompts import FOLLOWUP_DECIDER_PROMPT, get_shopping_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("products.pkl", "rb") as f:
    metadata = pickle.load(f)

df = metadata["df"]
emb_matrix = metadata["embeddings"]

index = faiss.read_index("product_index.faiss")
DIM = index.d

def embed_query(text: str):
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
        config={"output_dimensionality": DIM}
    )
    return np.array(response.embeddings[0].values, dtype="float32").reshape(1, -1)

def decide_followup(history, user_message):
    combined = f"History: {history}\nUser: {user_message}"
    out = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[FOLLOWUP_DECIDER_PROMPT, combined]
    )
    import json
    return json.loads(out.text)

def rag_search(session_id, user_message):
    history = get_history(session_id)
    d = decide_followup(history, user_message)

    if d["need_followup"]:
        return {
            "assistant_message": d["followup_question"],
            "products": []
        }

    query_emb = embed_query(user_message)
    scores, idxs = index.search(query_emb, 3)

    results = []
    for i, idx in enumerate(idxs[0]):
        row = df.iloc[idx]
        pdid = row["product_id"]
        results.append({
            "name": row["Product Name"],
            "subtitle": row.get("Subtitle", ""),
            "price": float(row.get("Price", 0) or 0),
            "url": row.get("URL", ""),
            "image_path": f"{pdid}.png",
            "similarity": float(scores[0][i])
        })

    prompt = f"User: {user_message}\nProducts: {results}"
    msg = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[get_shopping_prompt(), prompt]
    )

    return {
        "assistant_message": msg.text,
        "products": results
    }
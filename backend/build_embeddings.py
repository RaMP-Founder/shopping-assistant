import os
import pickle
import numpy as np
import pandas as pd
import faiss
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

client = genai.Client(api_key=API_KEY)

CSV_FILE = "minimalist_all_products_with_ids.csv"
EMBED_MODEL = "text-embedding-004"
EMBED_DIM = 256   # FORCE 256


TEXT_COLUMNS = [
    "Product Name",
    "Subtitle",
    "Description",
    "What Makes It Potent",
    "Ideal For"
]

def combine_text(row):
    parts = []
    for col in TEXT_COLUMNS:
        val = row.get(col, "")
        if pd.notna(val):
            parts.append(str(val))
    return " ".join(parts)

def get_embedding(text: str):
    if not text:
        text = ""

    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text,
        config={"output_dimensionality": EMBED_DIM}   # KEY FIX
    )

    return np.array(response.embeddings[0].values, dtype=np.float32)


def build_index():
    df = pd.read_csv(CSV_FILE)
    df["combined"] = df.apply(combine_text, axis=1)

    embeddings = []

    for i, txt in enumerate(df["combined"]):
        print(f"Embedding {i+1}/{len(df)}")
        emb = get_embedding(txt)
        embeddings.append(emb)

    matrix = np.vstack(embeddings).astype("float32")

    print("Final embedding dim:", matrix.shape[1])

    index = faiss.IndexFlatL2(EMBED_DIM)
    index.add(matrix)

    faiss.write_index(index, "product_index.faiss")

    with open("products.pkl", "wb") as f:
        pickle.dump({"df": df, "embeddings": matrix}, f)

    print("Saved product_index.faiss and products.pkl")

if __name__ == "__main__":
    build_index()
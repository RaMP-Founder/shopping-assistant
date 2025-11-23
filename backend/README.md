Backend instructions:

1. Create and activate python venv at project root:
   python3 -m venv ../chatbot_env
   source ../chatbot_env/bin/activate

2. Install:
   pip install --upgrade pip
   pip install -r requirements.txt

3. Place your products.pkl and product_index.faiss in this backend folder.
   products.pkl should contain a dict with keys: 'df' (pandas DataFrame) and 'embeddings' (numpy array).

4. Put product images into the product_images/ folder.

5. Copy .env.example to .env and add GEMINI_API_KEY.

6. Run:
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload

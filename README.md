# shopping-assistant


Structure:
- backend/: FastAPI backend, expects products.pkl and product_index.faiss in backend folder and product_images/ containing images.
- frontend/: React + Tailwind premium UI, will call backend at http://localhost:8000/chat

Quick start:
1. Create python venv at repo root:
   python3 -m venv chatbot_env
   source chatbot_env/bin/activate

2. Backend:
   cd backend
   pip install --upgrade pip
   pip install -r requirements.txt
   copy your products.pkl and product_index.faiss into backend/
   place product images into backend/product_images/
   copy .env.example to .env and fill GEMINI_API_KEY
   uvicorn api:app --reload --host 0.0.0.0 --port 8000

3. Frontend:
   cd frontend
   nvm use 18
   npm install
   npm start

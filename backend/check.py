import pickle, faiss

print("Checking embeddings...")
with open("products.pkl","rb") as f:
    d=pickle.load(f)

emb = d["embeddings"]
print("Embeddings shape:", emb.shape)

index = faiss.read_index("product_index.faiss")
print("FAISS index dimension:", index.d)
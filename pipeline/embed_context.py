import os
from chromadb import PersistentClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from uuid import uuid4

# Setup paths
base_dir = os.path.dirname(os.path.dirname(__file__))
context_path = os.path.join(base_dir, "graphdb", "context.txt")
chroma_dir = os.path.join(base_dir, "vector_store")

# Step 1: Load context facts
with open(context_path, "r", encoding="utf-8") as f:
    facts = [line.strip() for line in f if line.strip()]

# Step 2: Embed facts using SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(facts).tolist()

# Step 3: Initialize ChromaDB collection
client = PersistentClient(path=chroma_dir)
collection = client.get_or_create_collection("context_facts")

# Step 4: Insert embedded facts into Chroma
collection.add(
    documents=facts,
    embeddings=embeddings,
    ids=[str(uuid4()) for _ in facts]
)

print(f"✅ Embedded and stored {len(facts)} facts in ChromaDB at: {chroma_dir}")
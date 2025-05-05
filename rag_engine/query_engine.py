import os
from llm_utils.ollama_api import query_llama3
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings
import streamlit as st
# Step 1: Semantic retrieval of top-k facts using ChromaDB + scores
def retrieve_relevant_facts(question, top_k=5):
    @st.cache_resource
    def load_embedder():
        return SentenceTransformer("all-MiniLM-L6-v2")

    model = load_embedder()
    question_vector = model.encode([question])[0].tolist()

    base_dir = os.path.dirname(os.path.dirname(__file__))
    chroma_dir = os.path.join(base_dir, "vector_store")
    client = Client(Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection("context_facts")

    results = collection.query(
        query_embeddings=[question_vector],
        n_results=top_k,
        include=["documents", "distances"]
    )

    docs = results["documents"][0]
    distances = results["distances"][0]
    # Convert distance to similarity (1 - distance)
    scored_facts = [(doc, round(1 - dist, 3)) for doc, dist in zip(docs, distances)]
    return scored_facts

# Step 2: Build LLaMA prompt and return both answer + facts
def answer_question(question):
    scored_facts = retrieve_relevant_facts(question)

    prompt = "Use the following facts to answer the question.\n\n"
    for fact, _ in scored_facts:
        prompt += f"- {fact}\n"
    prompt += f"\nQ: {question}\nA:"

    answer = query_llama3(prompt)
    return answer, scored_facts

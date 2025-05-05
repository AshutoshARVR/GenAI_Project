import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag_engine.query_engine import answer_question

# Streamlit App Config
st.set_page_config(page_title="EDP4E GenAI", page_icon="🧠", layout="wide")

# Miami Pink & London Blue Styling
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #0d0d0d;
        color: #ffffff;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3, h4 {
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: white;
    }
    .stButton > button {
        background-color: #e91e63;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .chat-bubble {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 6])
with col1:
    st.image("frontend/jlr_logo.png", width=70)
with col2:
    st.title("EDP4E Semantic GenAI Assistant")
    st.markdown("Ask questions about assets, engineers, or test data sources.")
    st.markdown("**🤖 Model: Mixtral-8x7B via Together.ai API**")

# Chat state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear chat button
if st.button("🧹 Clear Conversation"):
    st.session_state.chat_history = []

st.markdown("---")
st.markdown("## 💬 Ask a Question")

# Input
question = st.text_input("", placeholder="e.g., What kind of engineer is Alice")

# Handle question
if question:
    with st.spinner("🧠 Thinking..."):
        context_memory = ""
        for entry in st.session_state.chat_history:
            context_memory += f"Q: {entry['question']}\nA: {entry['answer']}\n"

        full_question = context_memory + f"\nQ: {question}"
        answer, scored_facts = answer_question(full_question)

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer.strip(),
            "facts": scored_facts
        })

# Chat Display
if st.session_state.chat_history:
    st.markdown("## 📜 Chat History")
    for entry in reversed(st.session_state.chat_history):
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown(f"### ❓ {entry['question']}")
            st.markdown(f"<div class='chat-bubble'>🤖 {entry['answer']}</div>", unsafe_allow_html=True)
        with col_right:
            st.markdown("### 🧾 Top Supporting Facts")
            for fact, score in entry["facts"]:
                st.markdown(f"- **({round(score, 3)})** {fact}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #FF5CA2;'>"
    "🚀 Powered by <b>Together.ai</b> using Mixtral-8x7B"
    "</div>",
    unsafe_allow_html=True
)
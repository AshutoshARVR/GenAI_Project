import requests
import streamlit as st


def query_llama3(prompt: str) -> str:
    api_key = st.secrets["TOGETHER_API_KEY"]
    model = st.secrets.get("LLM_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": ["</s>"]
    }

    response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        return f"[❌ Error from Together.ai]\n{response.text}"

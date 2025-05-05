import requests
import json

def query_llama3(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=True
    )
    result = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            result += data["response"]
    return result
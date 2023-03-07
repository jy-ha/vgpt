import requests
import json
from config import OPENAI_API_KEY


def gpt3_text_completion(
    text, model="text-babbage-001", max_tokens=256, temperature=0.5
):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY,
    }
    data = {
        "model": model,  # text-babbage-001, text-curie-001, text-davinci-003
        "prompt": text,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data))
    resp = json.loads(resp.text)
    try:
        return resp["choices"][0]["text"].strip()
    except Exception:
        return resp


def gpt_chat(text, max_tokens=1024, temperature=1.0):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY,
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": text},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data))
    resp = resp.json()
    print(resp)
    try:
        return resp["choices"][0]["message"]["content"].strip()
    except Exception:
        return resp


def list_models():
    url = "https://api.openai.com/v1/models"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY,
    }
    resp = requests.get(url, headers=headers)
    resp = json.loads(resp.text)["data"]
    for model in resp:
        print(model["id"], "\t\t", str(model["permission"][0]["allow_fine_tuning"]))

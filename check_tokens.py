import os
import sys
import requests
from dotenv import load_dotenv

# Set encoding to utf-8 just in case
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load variables from .env
load_dotenv()

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    print("Error: HF_TOKEN is not set in your .env file!")
    exit(1)

model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"
url = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json"
}

payload = {
    "model": model_name,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Give me a short message of 5 words."}
    ],
    "max_tokens": 20
}

try:
    print(f"Sending request for {model_name} via raw HTTP to {url}...")
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Success! Response:")
        print(data["choices"][0]["message"]["content"].strip())
    else:
        print(f"\n❌ Error: Status Code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\n❌ Exception: {e}")

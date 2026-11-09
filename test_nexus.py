
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEXUS_API_KEY")
BASE_URL = os.getenv("NEXUS_BASE_URL")
MODEL = os.getenv("NEXUS_MODEL")

if not API_KEY:
    raise ValueError("NEXUS_API_KEY missing in .env")

if not BASE_URL:
    raise ValueError("NEXUS_BASE_URL missing in .env")

if not MODEL:
    raise ValueError("NEXUS_MODEL missing in .env")

url = f"{BASE_URL.rstrip('/')}/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": "Hello CareerBridge! Reply with a short greeting."
        }
    ],
    "temperature": 0.2
}

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    print("Status Code:", response.status_code)
    print("Response:")

    if response.ok:
        result = response.json()
        print(result["choices"][0]["message"]["content"])
    else:
        print(response.text)

except requests.exceptions.RequestException as error:
    print("Connection Error:", error)

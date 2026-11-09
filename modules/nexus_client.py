
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def nexus_chat(prompt, system_prompt="You are CareerBridge AI."):
    """
    Send a text prompt to Nexus AI and return the model response.
    """

    api_key = os.getenv("NEXUS_API_KEY")
    base_url = os.getenv("NEXUS_BASE_URL")
    model = os.getenv("NEXUS_MODEL")

    if not api_key or not base_url or not model:
        raise ValueError(
            "Nexus configuration missing. Check your .env file."
        )

    url = base_url.rstrip("/") + "/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Nexus API Error {response.status_code}: "
            f"{response.text[:500]}"
        )

    result = response.json()

    return result["choices"][0]["message"]["content"]

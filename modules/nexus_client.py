
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("NEXUS_API_KEY")
BASE_URL = os.getenv("NEXUS_BASE_URL")
MODEL = os.getenv("NEXUS_MODEL", "gpt-4.1-nano")


def nexus_chat(prompt, system_prompt="You are CareerBridge AI."):
    if not API_KEY:
        raise ValueError("NEXUS_API_KEY missing in .env")

    if not BASE_URL:
        raise ValueError("NEXUS_BASE_URL missing in .env")

    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL.rstrip("/") + "/v1"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

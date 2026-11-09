
import json
from modules.nexus_client import nexus_chat


def analyze_resume(resume_text, jd_text):

    system_prompt = """
You are CareerBridge, an evidence-based interview readiness assistant.

Rules:
- Never invent skills or experience.
- Use only information present in the resume.
- Do not make hiring decisions.
- Return ONLY valid JSON.
- Match skills based on evidence.
"""

    prompt = f"""
Analyze this resume against the job description.

RESUME:
{resume_text[:12000]}

JOB DESCRIPTION:
{jd_text[:8000]}

Return JSON in this exact structure:

{{
  "matched_skills": [],
  "missing_skills": [],
  "supported_claims": [],
  "weakly_supported_claims": [],
  "unsupported_claims": [],
  "summary": ""
}}
"""

    response = nexus_chat(prompt, system_prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Nexus returned invalid JSON.")

    required_keys = [
        "matched_skills",
        "missing_skills",
        "supported_claims",
        "weakly_supported_claims",
        "unsupported_claims",
        "summary"
    ]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing JSON field: {key}")

    return data

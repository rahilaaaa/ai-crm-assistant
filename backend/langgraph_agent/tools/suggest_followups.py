from langchain.tools import tool
from services.groq_llm import llm
import json


@tool
def suggest_followups(interaction: str):
    """Suggest follow-up actions for a doctor interaction."""

    prompt = f"""
You are a pharma CRM assistant.

Based on the interaction below, suggest 3 follow-up actions for the field representative.

Return ONLY valid JSON.

Format:
{{
  "followups": [
    "follow up action 1",
    "follow up action 2",
    "follow up action 3"
  ]
}}

Interaction:
{interaction}
"""

    response = llm.invoke(prompt)

    try:
        data = json.loads(response.content)
        return json.dumps(data)
    except Exception:
        return json.dumps({
            "followups": [
                "Schedule a follow-up visit with the doctor",
                "Share additional clinical evidence",
                "Check if the doctor needs patient samples"
            ]
        })
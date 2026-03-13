from langchain_core.tools import tool
from services.groq_llm import llm
import json
import re

from database import SessionLocal
from models import Interaction


@tool
def log_interaction(message: str):
    """Extract interaction information from text and store it in the database."""

    print("USER MESSAGE:", message)

    prompt = f"""
You are a CRM data extractor.

Extract structured CRM interaction data from the text.

Return ONLY raw JSON.

Fields:
hcp_name
interaction_type
meeting_date
meeting_time
attendees
topics
sentiment
materials_shared
outcomes
followups

If information is missing, return null.

Example output:

{{
 "hcp_name": "Dr Smith",
 "interaction_type": "meeting",
 "meeting_date": null,
 "meeting_time": null,
 "attendees": null,
 "topics": "diabetes treatment discussion",
 "sentiment": "positive",
 "materials_shared": "brochure",
 "outcomes": null,
 "followups": null
}}

Text:
{message}
"""

    # Disable tool calling inside the extractor
    llm_no_tools = llm.bind_tools([])

    response = llm_no_tools.invoke(prompt)

    content = response.content

    print("RAW LLM OUTPUT:", content)

    try:

        # Remove markdown if present
        content = content.replace("```json", "").replace("```", "")

        # Extract JSON block
        match = re.search(r"\{.*\}", content, re.S)

        if not match:
            raise ValueError("No JSON found in LLM output")

        data = json.loads(match.group())

    except Exception as e:

        print("JSON PARSE ERROR:", e)

        # fallback data
        data = {
            "hcp_name": None,
            "interaction_type": None,
            "meeting_date": None,
            "meeting_time": None,
            "attendees": None,
            "topics": message,
            "sentiment": None,
            "materials_shared": None,
            "outcomes": None,
            "followups": None,
        }

    print("PARSED DATA:", data)

    db = SessionLocal()

    try:

        interaction = Interaction(
            hcp_name=data.get("hcp_name"),
            interaction_type=data.get("interaction_type"),
            meeting_date=data.get("meeting_date"),
            meeting_time=data.get("meeting_time"),
            attendees=data.get("attendees"),
            topics=data.get("topics"),
            sentiment=data.get("sentiment"),
            materials_shared=data.get("materials_shared"),
            outcomes=data.get("outcomes"),
            followups=data.get("followups"),
        )

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

    finally:
        db.close()

    return {
    "hcp_name": interaction.hcp_name,
    "interaction_type": interaction.interaction_type,

    "meeting_date": str(interaction.meeting_date) if interaction.meeting_date else None,
    "meeting_time": str(interaction.meeting_time) if interaction.meeting_time else None,
    "attendees": interaction.attendees,
    "topics": interaction.topics,
    "sentiment": interaction.sentiment,
    "materials_shared": interaction.materials_shared,
    "outcomes": interaction.outcomes,
    "followups": interaction.followups,
}
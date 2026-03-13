from langchain_core.tools import tool
from services.groq_llm import llm
import json
import re

from database import SessionLocal
from models import Interaction


@tool
def edit_interaction(message: str, current_data: dict):
    """
    Update specific fields of an existing interaction.
    Only changed fields should be returned.
    """

    prompt = f"""
You are a CRM interaction editor.

Current interaction:
{current_data}

User correction:
{message}

Return the FULL corrected interaction JSON.

Rules:
- Use current values unless user corrected them
- Never return null values
- Do not remove fields

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

Example:

{{
 "hcp_name": "Dr John",
 "sentiment": "negative"
}}

If nothing changes return {{}}.
"""

    llm_no_tools = llm.bind_tools([])

    response = llm_no_tools.invoke(prompt)

    content = response.content

    try:

        content = content.replace("```json", "").replace("```", "")

        match = re.search(r"\{.*\}", content, re.S)

        updates = json.loads(match.group())

    except:
        updates = {}

    # Merge changes
    updated_data = current_data.copy()
    for key, value in updates.items():
            if value not in [None, "", "null"]:
                updated_data[key] = value
    db = SessionLocal()

    try:

        interaction = db.query(Interaction).order_by(Interaction.id.desc()).first()

        for key, value in updated_data.items():
            if getattr(interaction, key) != value:
                setattr(interaction, key, value)

        db.commit()
        db.refresh(interaction)

    finally:
        db.close()

    return updated_data



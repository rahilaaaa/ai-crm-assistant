from langchain_core.tools import tool
from services.groq_llm import llm
import json
import re


@tool
def recommend_materials(topic: str):
    """
    Recommend pharma marketing materials based on discussion topic.
    """

    prompt = f"""
You are a pharmaceutical marketing assistant.

Suggest useful marketing materials for a field representative.

Topic:
{topic}

Return JSON list.

Example:

{{
 "materials": [
   "Patient education brochure",
   "Clinical study summary",
   "Doctor visual aid",
   "Dosage guideline leaflet"
 ]
}}
"""

    llm_no_tools = llm.bind_tools([])

    response = llm_no_tools.invoke(prompt)

    content = response.content

    try:

        content = content.replace("```json", "").replace("```", "")

        match = re.search(r"\{.*\}", content, re.S)

        data = json.loads(match.group())

        return data

    except:

        return {
            "materials": [
                "Patient brochure",
                "Clinical study leaflet"
            ]
        }
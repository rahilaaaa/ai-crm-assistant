from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

from langchain_core.messages import HumanMessage
from langgraph_agent.agent import agent

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    form_data: dict = {}


def detect_action(text: str):
    text = text.lower()

    if any(word in text for word in ["log", "save", "submit", "record"]):
        return "log"

    if any(word in text for word in ["sorry", "actually", "correction", "update", "change"]):
        return "edit"

    if "follow up" in text or "next step" in text:
        return "followup"
    
    if any(word in text for word in ["history", "previous", "last meeting", "earlier"]):
        return "history"

    if any(word in text for word in ["recommend material", "marketing material"]):
        return "recommend"

    return "chat"


def is_edit_message(text: str):
    text = text.lower()

    edit_words = [
        "sorry",
        "actually",
        "correction",
        "update",
        "change",
        "wrong",
        "instead"
    ]

    return any(word in text for word in edit_words)


def format_assistant_message(data: dict):

    if "followups" in data:

        followups = data.get("followups")

        if not followups:
            return "Interaction logged successfully."

        if isinstance(followups, str):
            followups = [f.strip() for f in followups.split(",")]

        steps = "\n".join([f"• {s}" for s in followups])

        return f"Suggested follow-ups:\n{steps}"
     
    if "materials" in data:
        materials = "\n".join([f"• {m}" for m in data["materials"]])
        return f"Recommended materials:\n{materials}"

    if not data:
        return "I couldn't fully understand the message. Please describe the doctor interaction."

    hcp = data.get("hcp_name")
    interaction = data.get("interaction_type")
    date = data.get("meeting_date")

    if interaction and hcp and date:
        return f"Got it. I've logged your {interaction} with {hcp} on {date}."

    if hcp:
        return f"Thanks. I've updated the doctor name to {hcp}."

    return "Interaction updated."


@app.post("/chat")
async def chat(req: ChatRequest):

    action = detect_action(req.message)

    result = agent.invoke({
        "messages": [HumanMessage(content=req.message)],
        "form_data": req.form_data,
        "action": action
    })

    print("AGENT RESULT:", result)

    extracted_data = {}
    assistant_message = ""

    messages = result.get("messages", [])

    for msg in messages:
        if hasattr(msg, "content") and msg.content:
            try:
                data = json.loads(msg.content)

                if "materials" in data:
                    extracted_data = data
                    assistant_message = msg.content
                    break

                extracted_data = data

            except Exception:
                assistant_message = msg.content

    reply = format_assistant_message(extracted_data)

    if "Previous interactions" in assistant_message:
        reply = assistant_message

    response = {
        "message": reply,
        "data": extracted_data
    }

    return response
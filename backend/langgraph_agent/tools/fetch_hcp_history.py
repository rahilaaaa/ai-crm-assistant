from langchain.tools import tool
from database import SessionLocal
from models import Interaction
from datetime import date

@tool
def fetch_hcp_history(hcp_name: str):
    """
    Fetch previous interactions for a given HCP.
    """

    db = SessionLocal()

    try:
        interactions = (
        db.query(Interaction).filter(
        Interaction.hcp_name.ilike(f"%{hcp_name}%"),
        Interaction.meeting_date <= date.today()
        )
        .order_by(Interaction.meeting_date.desc())
        .limit(5)
        .all()
        )

        if not interactions:
            return f"No previous interactions found for {hcp_name}"

        history_text = f"Previous interactions with {hcp_name}:\n\n"

        for i in interactions:
            history_text += (
                f"Date: {i.meeting_date}\n"
                f"Type: {i.interaction_type}\n"
                f"Topics: {i.topics}\n"
                f"Sentiment: {i.sentiment}\n"
                f"Outcome: {i.outcomes}\n"
                f"------------------\n"
            )

        return history_text

    finally:
        db.close()




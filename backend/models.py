from sqlalchemy import Column, Integer, String, Date, Time, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Interaction(Base):

    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True)

    hcp_name = Column(String)
    interaction_type = Column(String)
    meeting_date = Column(Date)
    meeting_time = Column(Time)

    attendees = Column(Text)
    topics = Column(Text)

    materials_shared = Column(Text)
    samples_distributed = Column(Text)

    sentiment = Column(String)
    outcomes = Column(Text)
    followups = Column(Text)
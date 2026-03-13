from typing import TypedDict, Optional, Dict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    message: str
    form_data: Dict
    messages: List[BaseMessage]
    action: Optional[str]
    result: Optional[Dict]
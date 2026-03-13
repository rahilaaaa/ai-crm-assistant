from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from langchain_core.messages import SystemMessage

from services.groq_llm import llm

from .state import AgentState

from .tools.log_interaction import log_interaction
from .tools.edit_interaction import edit_interaction
from .tools.suggest_followups import suggest_followups
from .tools.fetch_hcp_history import fetch_hcp_history
from .tools.recommend_materials import recommend_materials


# -----------------------------
# TOOLS
# -----------------------------
tools = [
    log_interaction,
    edit_interaction,
    suggest_followups,
    fetch_hcp_history,
    recommend_materials
]

tool_node = ToolNode(tools)


# -----------------------------
# GRAPH
# -----------------------------
graph = StateGraph(AgentState)

llm_with_tools = llm.bind_tools(tools)


# -----------------------------
# LLM NODE
# -----------------------------
def call_llm(state: AgentState):

    messages = state["messages"]
    form_data = state.get("form_data", {})

    system_prompt = f"""
You are an AI CRM assistant for a field representative.

Current form data:
{form_data}

Available tools:

1. log_interaction
Use when the user describes a new meeting or call.

Arguments:
{{
 "message": "<user message>"
}}

2. edit_interaction
Use when the user corrects or updates existing form data.

Arguments:
{{
 "message": "<user message>",
 "current_data": {form_data}
}}

3. fetch_hcp_history
Use when the user refers to a doctor they visited before or says words like:
"again", "previous", "last time", "before".

Arguments:
{{
 "hcp_name": "<doctor name>"
}}

4. recommend_materials
Use when the user asks for marketing materials or suggestions for a medical topic.

Examples:
- "Recommend materials for diabetes discussion"
- "What materials should I take for hypertension meeting?"

Arguments:
{{
 "topic": "<medical topic>"
}}


5. suggest_followups
Do NOT call suggest_followups when the user is only logging an interaction.
Only call suggest_followups if the user explicitly asks for next steps or follow-ups.

Examples:
- "What should be my next step?"
- "Suggest follow ups"
- "What should I do after this meeting?"

Arguments:
{{
 "interaction": "<interaction summary>"
}}
Always call the correct tool.
"""
    response = llm_with_tools.invoke(
    [SystemMessage(content=system_prompt + f"\nCurrent form data:\n{form_data}")] + messages
)

    return {
        "messages": messages + [response]
    }


# -----------------------------
# ROUTER
# -----------------------------
def should_use_tool(state: AgentState):

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return "end"


# -----------------------------
# ADD NODES
# -----------------------------
graph.add_node("llm", call_llm)

graph.add_node("tools", tool_node)


# -----------------------------
# ENTRY POINT
# -----------------------------
graph.set_entry_point("llm")


# -----------------------------
# ROUTING
# -----------------------------
graph.add_conditional_edges(
    "llm",
    should_use_tool,
    {
        "tools": "tools",
        "end": "__end__"
    }
)


# After tool execution → finish
graph.add_edge("tools", "__end__")


# -----------------------------
# COMPILE
# -----------------------------
agent = graph.compile()

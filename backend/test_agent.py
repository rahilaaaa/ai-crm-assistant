from langgraph_agent.agent import agent

response = agent.invoke({
    "message": "Today I met Dr Smith and discussed product X efficiency. Sentiment was positive and I shared brochures."
})

print(response)
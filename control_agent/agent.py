# create a control agent that will call either search agent or multi tool agent

from google.adk.agents import Agent
from google.adk.tools import agent_tool
from search_agent import root_agent as search_agent
from multi_tool_agent import root_agent as multi_tool_agent
from inventory_agent import root_agent as inventory_agent

root_agent = Agent(
    name="control_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a control agent that can call either the search agent or the multi tool agent. "
        "You will decide which agent to call based on the user's question."
        "If the question is about the time or weather in a city, call the multi tool agent. "
        "If the question is about a student, call the student agent. "
        "If the question is about an inventory item, call the inventory agent."
    ),
    tools=[agent_tool.AgentTool(agent=search_agent), 
           agent_tool.AgentTool(agent=multi_tool_agent), 
           agent_tool.AgentTool(agent=inventory_agent)],
)

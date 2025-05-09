from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    tools=[google_search],
)

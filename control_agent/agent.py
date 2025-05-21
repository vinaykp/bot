# create a control agent that will call either search agent or multi tool agent

import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from search_agent import root_agent as search_agent
from inventory_agent import root_agent as inventory_agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

root_agent = Agent(
    name="control_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to control other agents."
    ),
    instruction=(
        "You will decide which actions to take based on the user's question. "
        "If the question is about the time or weather in a city, use your built-in tools. "
        "If the question is about a general search, call the search agent. "
        "If the question is about an inventory item, call the inventory agent."
    ),
    tools=[
        get_weather,
        get_current_time,
        agent_tool.AgentTool(agent=search_agent),
        agent_tool.AgentTool(agent=inventory_agent)
    ],
)

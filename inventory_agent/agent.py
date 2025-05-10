from inventory_agent.inventory import create_item
from inventory_agent.inventory import read_item
from inventory_agent.inventory import read_all_items
from inventory_agent.inventory import update_item
from inventory_agent.inventory import delete_item

from google.adk.agents import Agent
from google.genai import types 
from google.adk.agents.callback_context import CallbackContext
from typing import Optional
from google.adk.models import LlmRequest, LlmResponse

# --- Define your callback function ---# Create callbacks instance
def check_sesnitive_items(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")
    sensitive_items = ["weapon", "drug", "explosive", "illegal", "controlled substance"]
    # Inspect the last user message in the request contents
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
         if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback] Inspecting last user message: '{last_user_message}'")
    # last_user_message is not None and contains any of the sensitive items
    if last_user_message is not None and any(word in last_user_message for word in sensitive_items) and ("create" in last_user_message or "add" in last_user_message):
        print("[Callback] Sensitive item detected. Skipping LLM call.")
        # Return an LlmResponse to skip the actual LLM call
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="I apologize, but I cannot assist with adding sensitive or restricted items to the inventory.")],
            )
        )
    else:
        print("[Callback] Proceeding with LLM call.")
        # Return None to allow the (modified) request to go to the LLM
        return None


# --- Google ADK Agent Definition ---
root_agent = Agent(
    name="sqlite_inventory_manager_agent",
    model="gemini-2.0-flash-exp", # Or your preferred Gemini model
    description="An agent that manages an inventory of items using an SQLite database. It can perform Create, Read, Update, and Delete (CRUD) operations.",
    instruction="""
        "You are an efficient inventory management assistant backed by a persistent SQLite database. "
        "You can create new items, read existing items by their ID, list all items (with optional filters for category, min_price, and max_price), "
        "update item details, and delete items from the inventory. "
        "When creating an item, ensure you have at least a 'name'. Ask for other details like 'price' and 'category' if not provided but useful. "
        "All data is persistent. Always confirm actions taken (creation, update, deletion) and provide clear feedback, including item IDs when relevant. "
        "If a user asks to 'get all items', 'list items', or 'show inventory', use the 'read_all_items' tool. "
        "Be precise with IDs for read, update, and delete operations. If an ID is not found, clearly state that."
        "When updating, only change the fields specified by the user."
    """,
    tools=[
        create_item,
        read_item,
        read_all_items,
        update_item,
        delete_item
    ],
    before_model_callback=check_sesnitive_items,
)


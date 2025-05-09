from google.adk.agents import Agent

from inventory_agent.inventory import create_item
from inventory_agent.inventory import read_item
from inventory_agent.inventory import read_all_items
from inventory_agent.inventory import update_item
from inventory_agent.inventory import delete_item


# --- Google ADK Agent Definition ---
# Ensure your environment is set up for Google Generative AI (e.g., GOOGLE_API_KEY or Vertex AI authentication).
root_agent = Agent(
    name="sqlite_inventory_manager_agent",
    model="gemini-2.0-flash-exp", # Or your preferred Gemini model
    description="An agent that manages an inventory of items using an SQLite database. It can perform Create, Read, Update, and Delete (CRUD) operations.",
    instruction=(
        "You are an efficient inventory management assistant backed by a persistent SQLite database. "
        "You can create new items, read existing items by their ID, list all items (with optional filters for category, min_price, and max_price), "
        "update item details, and delete items from the inventory. "
        "When creating an item, ensure you have at least a 'name'. Ask for other details like 'price' and 'category' if not provided but useful. "
        "All data is persistent. Always confirm actions taken (creation, update, deletion) and provide clear feedback, including item IDs when relevant. "
        "If a user asks to 'get all items', 'list items', or 'show inventory', use the 'read_all_items' tool. "
        "Be precise with IDs for read, update, and delete operations. If an ID is not found, clearly state that."
        "When updating, only change the fields specified by the user."
    ),
    tools=[
        create_item,
        read_item,
        read_all_items,
        update_item,
        delete_item
    ]
)


import sqlite3
import uuid
import json
from typing import Dict, Any, Optional, List

# --- SQLite Database Configuration ---
DB_NAME = "inventory_sqlite.db"

def init_db():
    """Initializes the SQLite database and creates the items table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL,
                category TEXT,
                additional_data TEXT -- To store other fields as a JSON string
            )
        """)
        conn.commit()
    print(f"Database '{DB_NAME}' initialized.")

# Call init_db when the script loads to ensure the table exists
init_db()

# --- Helper functions for database interaction ---
def _serialize_additional_data(data: Dict[str, Any]) -> str:
    """Serializes a dictionary to a JSON string for storing."""
    return json.dumps(data)

def _deserialize_additional_data(json_str: Optional[str]) -> Dict[str, Any]:
    """Deserializes a JSON string back to a dictionary."""
    if json_str:
        return json.loads(json_str)
    return {}

def _dict_factory(cursor, row):
    """Converts database rows to dictionaries, including deserializing additional_data."""
    d = {"id": row[0], "name": row[1], "price": row[2], "category": row[3]}
    additional = _deserialize_additional_data(row[4])
    d.update(additional) # Merge additional data into the main dictionary
    # Ensure 'id' from the main column is preserved, not overwritten by additional_data
    d["id"] = row[0]
    return d


# --- CRUD Function Tools (SQLite Version) ---

def create_item(item_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new item with the provided data and stores it in the SQLite database.

    Args:
        item_data (Dict[str, Any]): A dictionary containing the data for the new item.
                                     Must include 'name'. Other common fields: 'price', 'category'.
                                     Example: {"name": "Laptop", "price": 1200, "category": "Electronics", "stock": 50}

    Returns:
        Dict[str, Any]: A dictionary containing the ID of the newly created item and a status message.
    """
    print(f"--- Tool: create_item (SQLite) called with data: {item_data} ---")
    if not isinstance(item_data, dict) or not item_data:
        return {"status": "error", "message": "Item data must be a non-empty dictionary."}
    if 'name' not in item_data or not item_data['name']:
        return {"status": "error", "message": "Item 'name' is required and cannot be empty."}

    item_id = str(uuid.uuid4())
    name = item_data.pop('name')
    price = item_data.pop('price', None)
    category = item_data.pop('category', None)
    additional_data_json = _serialize_additional_data(item_data) # Remaining data

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO items (id, name, price, category, additional_data)
                VALUES (?, ?, ?, ?, ?)
            """, (item_id, name, price, category, additional_data_json))
            conn.commit()
        return {"status": "success", "item_id": item_id, "message": f"Item '{name}' created with ID: {item_id}."}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"SQLite error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to create item: {str(e)}"}

def read_item(item_id: str) -> Dict[str, Any]:
    """
    Retrieves an item by its ID from the SQLite database.

    Args:
        item_id (str): The unique identifier of the item to retrieve.

    Returns:
        Dict[str, Any]: A dictionary containing the item's data if found, or an error message.
    """
    print(f"--- Tool: read_item (SQLite) called for ID: {item_id} ---")
    if not item_id or not isinstance(item_id, str):
        return {"status": "error", "message": "Invalid item ID provided. It must be a string."}

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = _dict_factory # Use custom row factory
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price, category, additional_data FROM items WHERE id = ?", (item_id,))
            item = cursor.fetchone()

        if item:
            return {"status": "success", "item": item}
        else:
            return {"status": "error", "message": f"Item with ID '{item_id}' not found."}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"SQLite error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to read item: {str(e)}"}


def read_all_items(category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None) -> Dict[str, Any]:
    """
    Retrieves all items from SQLite, optionally filtering by category, min_price, and/or max_price.

    Args:
        category (Optional[str]): The category to filter items by.
        min_price (Optional[float]): The minimum price to filter items by.
        max_price (Optional[float]): The maximum price to filter items by.

    Returns:
        Dict[str, Any]: A dictionary containing a list of items or an error message.
    """
    print(f"--- Tool: read_all_items (SQLite) called with category: {category}, min_price: {min_price}, max_price: {max_price} ---")
    query = "SELECT id, name, price, category, additional_data FROM items"
    conditions = []
    params = []

    if category:
        conditions.append("LOWER(category) = LOWER(?)")
        params.append(category)
    if min_price is not None:
        conditions.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        conditions.append("price <= ?")
        params.append(max_price)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = _dict_factory # Use custom row factory
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            items = cursor.fetchall()

        if not items:
            message = "No items found matching your criteria." if params else "There are no items in the store yet."
            return {"status": "success", "items": [], "message": message}
        return {"status": "success", "items": items}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"SQLite error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to read items: {str(e)}"}

def update_item(item_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates an existing item in SQLite with new data. Only provided fields are updated.

    Args:
        item_id (str): The unique identifier of the item to update.
        update_data (Dict[str, Any]): A dictionary containing the fields to update and their new values.
                                     Cannot update 'id'.

    Returns:
        Dict[str, Any]: A dictionary confirming the update or an error message.
    """
    print(f"--- Tool: update_item (SQLite) called for ID: {item_id} with data: {update_data} ---")
    if not item_id or not isinstance(item_id, str):
        return {"status": "error", "message": "Invalid item ID provided."}
    if not isinstance(update_data, dict) or not update_data:
        return {"status": "error", "message": "Update data must be a non-empty dictionary."}
    if "id" in update_data and update_data["id"] != item_id: # Prevent changing ID
         return {"status": "error", "message": "Cannot change item ID during update."}
    update_data.pop("id", None) # Remove id from update_data if present

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row # For easier access to current additional_data
            cursor = conn.cursor()

            # Check if item exists
            cursor.execute("SELECT additional_data FROM items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            if not row:
                return {"status": "error", "message": f"Item with ID '{item_id}' not found for update."}

            current_additional_dict = _deserialize_additional_data(row["additional_data"])

            set_clauses = []
            params = []

            # Standard fields
            if "name" in update_data:
                set_clauses.append("name = ?")
                params.append(update_data.pop("name"))
            if "price" in update_data:
                set_clauses.append("price = ?")
                params.append(update_data.pop("price"))
            if "category" in update_data:
                set_clauses.append("category = ?")
                params.append(update_data.pop("category"))

            # Update additional_data (remaining fields in update_data)
            if update_data: # If there are still fields in update_data, they go into additional_data
                current_additional_dict.update(update_data)
                set_clauses.append("additional_data = ?")
                params.append(_serialize_additional_data(current_additional_dict))
            elif not current_additional_dict and not update_data and "additional_data" not in [c.split("=")[0].strip() for c in set_clauses]:
                # If there was no additional data and no new additional data is being added,
                # ensure it's not accidentally set if it wasn't touched.
                # This case is mostly handled by how update_data is consumed.
                pass


            if not set_clauses:
                return {"status": "info", "message": "No valid fields provided for update."}

            query = f"UPDATE items SET {', '.join(set_clauses)} WHERE id = ?"
            params.append(item_id)

            cursor.execute(query, tuple(params))
            conn.commit()

            if cursor.rowcount == 0: # Should have been caught by the select earlier
                return {"status": "error", "message": f"Item with ID '{item_id}' not found for update (race condition?)."}

        # Fetch the updated item to return it
        updated_item_response = read_item(item_id)
        if updated_item_response["status"] == "success":
            return {"status": "success", "item_id": item_id, "message": f"Item '{item_id}' updated successfully.", "updated_item": updated_item_response["item"]}
        else: # Should not happen if update was successful
            return {"status": "warning", "item_id": item_id, "message": f"Item '{item_id}' updated, but failed to retrieve afterwards."}

    except sqlite3.Error as e:
        return {"status": "error", "message": f"SQLite error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to update item: {str(e)}"}


def delete_item(item_id: str) -> Dict[str, Any]:
    """
    Deletes an item by its ID from the SQLite database.

    Args:
        item_id (str): The unique identifier of the item to delete.

    Returns:
        Dict[str, Any]: A dictionary confirming the deletion or an error message.
    """
    print(f"--- Tool: delete_item (SQLite) called for ID: {item_id} ---")
    if not item_id or not isinstance(item_id, str):
        return {"status": "error", "message": "Invalid item ID provided."}

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Optionally, retrieve name before deleting for a more informative message
            cursor.execute("SELECT name FROM items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            item_name = row[0] if row else "Unknown"

            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()

            if cursor.rowcount > 0:
                return {"status": "success", "item_id": item_id, "message": f"Item '{item_name}' (ID: {item_id}) deleted successfully."}
            else:
                return {"status": "error", "message": f"Item with ID '{item_id}' not found for deletion."}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"SQLite error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete item: {str(e)}"}

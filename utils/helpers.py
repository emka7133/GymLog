from datetime import datetime

def add(data, new_item):
    """Add a new item"""
    if any(item["id"] == new_item["id"] for item in data):
        raise ValueError(f"Item with id '{new_item['id']}' already exists.")
    
    now = datetime.now().isoformat(timespec="seconds")
    new_item["created_at"] = now
    new_item["last_updated"] = now
    data.append(new_item)
    return data, new_item

def edit(data, item_id, updates):
    """Edit an existing item by id and update timestamp."""
    for item in data:
        if item["id"] == item_id:
            item.update(updates)
            item["last_updated"] = datetime.now().isoformat(timespec="seconds")
            return data, item_id
    raise ValueError(f"No item found with id '{item_id}'")

def remove(data, item_id):
    """Remove an item by id."""
    updated = [item for item in data if item["id"] != item_id]
    if len(updated) == len(data):
        raise ValueError(f"No item found with id '{item_id}'")
    return updated, item_id

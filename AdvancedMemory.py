import json
import os

MEMORY_FILE = "conversation_history.json"

def save_memory(history):
    """
    Saves the conversation history to a persistent JSON file.
    :param history: The conversation history as a string.
    """
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump({"history": history}, f, indent=2)
        print("Memory saved successfully.")
    except Exception as e:
        print("Error saving memory:", e)

def load_memory():
    """
    Loads the conversation history from the persistent JSON file.
    :return: The conversation history as a string. Returns an empty string if the file does not exist.
    """
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
            return data.get("history", "")
        except Exception as e:
            print("Error loading memory:", e)
            return ""
    return ""

def update_memory(new_entry):
    """
    Appends a new entry to the conversation history and saves the updated history.
    :param new_entry: The new conversation entry as a string.
    :return: The updated conversation history.
    """
    current_history = load_memory()
    if current_history:
        updated_history = current_history + "\n" + new_entry
    else:
        updated_history = new_entry
    save_memory(updated_history)
    return updated_history

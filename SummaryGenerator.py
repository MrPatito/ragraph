def generate_conversation_summary(history):
    # Basic summary generation logic; in a real scenario, you might call an LLM or implement more advanced logic.
    if not history:
        return "No conversation history available."
    # For now, simply truncate the history as a 'summary'
    return f"Summary (first 200 chars): {history[:200]}... "

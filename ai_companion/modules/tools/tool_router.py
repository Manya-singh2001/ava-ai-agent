def detect_tool(user_input: str):
    text = user_input.lower()

    if "weather" in text:
        return "weather"

    if "search" in text or "who is" in text or "what is" in text:
        return "search"

    return None

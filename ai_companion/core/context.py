def trim_messages(messages, max_messages=10):
    """
    Keep system + recent messages.
    """
    system_messages = [m for m in messages if m.type == "system"]
    other_messages = [m for m in messages if m.type != "system"]

    trimmed = other_messages[-max_messages:]

    return system_messages + trimmed
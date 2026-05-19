class SimpleMemory:
    def __init__(self):
        self.memory = {}

    def update(self, message: str):
        message = message.lower()

        # very basic extraction
        if "my name is" in message:
            name = message.split("my name is")[-1].strip().split()[0]
            self.memory["name"] = name

    def get_context(self) -> str:
        if not self.memory:
            return ""

        context = []
        if "name" in self.memory:
            context.append(f"User's name is {self.memory['name']}")

        return "\n".join(context)
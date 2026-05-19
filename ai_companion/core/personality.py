from ai_companion.core.prompts import CHARACTER_CARD_PROMPT
from ai_companion.modules.memory.long_term.memory_manager import get_memory_manager
from ai_companion.core.context_generation import ActivityGenerator


def build_personality_prompt(user_message: str):
    memory_manager = get_memory_manager()
    activity_generator = ActivityGenerator()

    memories = memory_manager.retrieve(user_message)

    memory_context = "\n".join(memories[:5]) 
    current_activity = activity_generator.get_activity()

    return CHARACTER_CARD_PROMPT.format(
        memory_context=memory_context,
        current_activity=current_activity
    )
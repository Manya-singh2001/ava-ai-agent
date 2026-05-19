from langchain_groq import ChatGroq
from ai_companion.settings import settings


class ConversationSummarizer:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.SMALL_TEXT_MODEL_NAME,
            api_key=settings.GROQ_API_KEY,
            temperature=0
        )

    async def summarize(self, messages):
        text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

        prompt = f"""
Summarize the following conversation into a concise memory.
Keep key facts, preferences, and context.

Conversation:
{text}

Summary:
"""

        response = await self.llm.ainvoke(prompt)
        return response.content
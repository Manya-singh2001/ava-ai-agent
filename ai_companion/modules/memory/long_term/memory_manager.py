from ai_companion.modules.memory.long_term.vector_store import QdrantVectorStore
from ai_companion.core.prompts import MEMORY_ANALYSIS_PROMPT
from langchain_groq import ChatGroq
from ai_companion.settings import settings
import json


class MemoryManager:
    def __init__(self):
        self.store = QdrantVectorStore()

        self.llm = ChatGroq(
            model=settings.SMALL_TEXT_MODEL_NAME,
            api_key=settings.GROQ_API_KEY,
            temperature=0
        )

    async def analyze_and_store(self, user_id: str, message: str):
        prompt = MEMORY_ANALYSIS_PROMPT.format(message=message)

        response = await self.llm.ainvoke(prompt)

        try:
            data = json.loads(response.content)
        except Exception:
            print("Memory parsing failed:", response.content)
            return

    def _add_memory(self, user_id: str, memory: str, score: int):
        existing = self.store.search(user_id, memory, limit=5)

        # simple dedup
        for item in existing:
            if memory.lower() in item.lower():
                return

        self.store.add(user_id, memory, score)

    def retrieve(self, user_id: str, query: str):
        results = self.store.search(user_id, query, limit=5)

        # simple ranking
        results = [r["text"]for r in results]

        return results


# Singleton instance
memory_manager_instance = None


def get_memory_manager():
    global memory_manager_instance
    if memory_manager_instance is None:
        memory_manager_instance = MemoryManager()
    return memory_manager_instance
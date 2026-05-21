import json
from langchain_groq import ChatGroq
from ai_companion.settings import settings
from ai_companion.core.prompts import MEMORY_ANALYSIS_PROMPT
from ai_companion.modules.memory.long_term.vector_store import QdrantVectorStore


class MemoryManager:
    def __init__(self):
        self.store = QdrantVectorStore()

        self.llm = ChatGroq(
            model=settings.SMALL_TEXT_MODEL_NAME,
            api_key=settings.GROQ_API_KEY,
            temperature=0
        )

    async def analyze_and_store(self, user_id: str, message: str):
        try:
            prompt = MEMORY_ANALYSIS_PROMPT.format(message=message)

            response = await self.llm.ainvoke(prompt)

            data = json.loads(response.content)

            if data.get("is_important"):
                memory = data.get("formatted_memory")
                score = data.get("importance_score", 5)

                if memory:
                    self._add_memory(user_id, memory, score)

        except Exception as e:
            print("Memory parsing failed:", e)

    def _add_memory(self, user_id: str, memory: str, score: int):
        # ✅ Deduplication
        existing = self.store.search(user_id, memory, limit=5)

        for item in existing:
            if memory.lower() in item["text"].lower():
                return

        self.store.add(user_id, memory, score)

    def retrieve(self, user_id: str, query: str):
        try:
            results = self.store.search(user_id, query, limit=5)

            # Already ranked via decay
            return [r["text"] for r in results]

        except Exception as e:
            print("Memory retrieval failed:", e)
            return []


memory_manager_instance = None


def get_memory_manager():
    global memory_manager_instance
    if memory_manager_instance is None:
        memory_manager_instance = MemoryManager()
    return memory_manager_instance
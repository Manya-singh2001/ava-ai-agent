from langchain_groq import ChatGroq
from ai_companion.settings import settings

def get_chat_model():
    return ChatGroq(
        model=settings.TEXT_MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
        temperature=0.7
    )
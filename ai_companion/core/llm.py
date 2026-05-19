from langchain_groq import ChatGroq
from dotenv import load_dotenv 
import os 

from ai_companion.core.helpers import get_chat_model


def get_llm():
    return get_chat_model()

load_dotenv()

def get_model(temp=0.7):
    return ChatGroq(
        api_key = os.getenv("GROQ_API_KEY"),
        model_name = "llama3-8b-8192",
        temperature = temp,
    )
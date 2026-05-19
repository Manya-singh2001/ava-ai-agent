from langchain_core.messages import AIMessage, HumanMessage 
from ai_companion.core.helpers import get_chat_model
from langchain_core.messages import SystemMessage
from ai_companion.core.personality import build_personality_prompt
from ai_companion.core.prompts import CHARACTER_CARD_PROMPT
from ai_companion.core.prompts import ROUTER_PROMPT
from langchain_core.messages import SystemMessage, AIMessage
from ai_companion.graph.state import AppState
from ai_companion.modules.image.text_to_image import TextToImage
import time
from ai_companion.modules.memory.memory import SimpleMemory
from ai_companion.modules.memory.long_term.memory_manager import get_memory_manager
from ai_companion.modules.speech.text_to_speech import TextToSpeech
import os
from ai_companion.modules.memory.long_term.memory_manager import MemoryManager
from ai_companion.modules.memory.short_term.session_memory import get_session_memory
import edge_tts
import tempfile
from ai_companion.core.context import trim_messages 
from ai_companion.settings import settings
from ai_companion.modules.memory.short_term.summarizer import ConversationSummarizer
from ai_companion.modules.image.generator import ImageGenerator
from ai_companion.core.safe_llm import safe_ainvoke
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from ai_companion.core.context import trim_messages
from ai_companion.modules.tools.web_search import web_search
from ai_companion.modules.tools.weather import get_weather
from ai_companion.modules.tools.tool_router import detect_tool


image_generator = ImageGenerator()
memory_manager = MemoryManager()
model = get_chat_model()
memory = get_memory_manager()
tts = TextToSpeech()
session_memory = get_session_memory()
summarizer = ConversationSummarizer()


async def router_node(state: AppState):
    try:
        messages = state["messages"]
        user_input = messages[-1].content.lower()
        
        if any(word in user_input for word in ["weather", "search", "who is", "what is"]):
            return {"workflow": "tool"}

        decision = await safe_ainvoke(model, [
            {"role": "system", "content": ROUTER_PROMPT},
            *messages
        ])

        workflow = decision.content.strip().lower()

        if workflow not in ["conversation", "image", "audio"]:
            workflow = "conversation"

        return {"workflow": workflow}

    except Exception as e:
        print("Router error:", e)
        return {"workflow": "conversation"}
    
    
#     print("ROUTER DECISION:", workflow)
#     print("STATE AFTER ROUTER:", {
#     "messages": len(messages),
#     "workflow": workflow
# })
#     return {
#         "messages": messages,
#         "workflow": workflow
#     }

async def tool_node(state):
    user_input = state["messages"][-1].content

    tool = detect_tool(user_input)

    try:
        if tool == "weather":
            city = user_input.split()[-1]
            result = get_weather(city)

        elif tool == "search":
            result = web_search(user_input)

        else:
            result = "I couldn't find a tool for that."

    except Exception as e:
        result = f"Tool failed: {str(e)}"

    return {
        "messages": [AIMessage(content=result)]
    }


async def conversation_node(state: AppState):
    try:
        messages = state["messages"]

        response = await safe_ainvoke(model, messages)

        return {"messages": messages + [response]}

    except Exception as e:
        print("Conversation error:", e)
        return {
            "messages": [AIMessage(content="Something went wrong in conversation 😅")]
        }


async def image_node(state: AppState):
    try:
        user_id = state["user_id"]
        messages = state["messages"]

        chat_history = "\n".join([m.content for m in messages])

        result = await image_generator.generate(chat_history)

        response_text = f"{result['narrative']}\n\n🖼️ {result['image_url']}"

        return {
            "messages": [AIMessage(content=response_text)]
        }

    except Exception as e:
        print("Image error:", e)
        return {
            "messages": [AIMessage(content="⚠️ Couldn't generate image right now")]
        }
    
    
    
async def audio_node(state: AppState):
    try:
        text = state["messages"][-1].content

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            audio_path = f.name

        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-JennyNeural"
        )

        await communicate.save(audio_path)

        os.system(f"start {audio_path}")

        return {
            "messages": [AIMessage(content="🔊 Playing audio...")]
        }

    except Exception as e:
        print("Audio error:", e)
        return {
            "messages": [AIMessage(content="⚠️ Audio failed")]
        }
        
        
        


async def chat_node(state: AppState):
    try:
        messages = state["messages"]
        user_message = messages[-1].content
        user_id = state["user_id"]

        # 🧠 store user message
        session_memory.add_message(user_id, "user", user_message)

        # 🧠 long-term memory
        await memory_manager.analyze_and_store(user_id, user_message)

        # 🧠 get conversation
        recent_msgs = session_memory.get_recent_messages(user_id)

        # trim
        recent_msgs = trim_messages(recent_msgs, max_messages=10)

        # summarization
        if len(recent_msgs) > 15:
            summary = await summarizer.summarize(recent_msgs[:-5])

            session_memory.clear()
            session_memory.add_message(user_id, "system", summary)

            recent_msgs = session_memory.get_recent_messages(user_id)

        # 🎭 personality
        system_prompt = build_personality_prompt(user_message)

        # format messages
        formatted_msgs = []
        for msg in recent_msgs:
            if msg["role"] == "user":
                formatted_msgs.append(HumanMessage(content=msg["content"]))
            else:
                formatted_msgs.append(AIMessage(content=msg["content"]))

        final_messages = [SystemMessage(content=system_prompt)] + formatted_msgs

        # 🔥 SAFE STREAMING
        full_response = ""

        try:
            async for chunk in model.astream(final_messages):
                if hasattr(chunk, "content") and chunk.content:
                    full_response += chunk.content
        except Exception as e:
            print("Streaming error:", e)
            fallback = await safe_ainvoke(model, final_messages)
            full_response = fallback.content

        response = AIMessage(content=full_response)

        # store
        session_memory.add_message(user_id, "assistant", full_response)

        return {"messages": [response]}

    except Exception as e:
        print("Chat node error:", e)
        return {
            "messages": [AIMessage(content="uhh something broke on my side 😅")]
        }
        
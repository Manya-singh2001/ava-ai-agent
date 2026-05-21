import chainlit as cl
from langchain_core.messages import HumanMessage
from ai_companion.graph.graph import create_graph
import re

graph = create_graph()


@cl.on_chat_start
async def start():
    user_id = cl.user_session.get("id")

    if not user_id:
        user_id = str(id(cl.user_session))
        cl.user_session.set("id", user_id)

    await cl.Message(
    content="""
# 👋 Welcome to Ava

### Your Personal AI Companion

✨ Remembers you  
🎨 Creates images  
🧠 Thinks step-by-step  

---

**Try:**
- "Create an image of a cyberpunk city"
- "Remember that I like coffee"
- "Explain transformers simply"

---

💬 *What’s on your mind?*
""",
    author="Ava"
).send()


@cl.on_message
async def main(message: cl.Message):
    user_id = cl.user_session.get("id")

    msg = cl.Message(
        content="",
        author="Ava"
    )
    await msg.send()

    full_response = ""

    # Thinking indicator
    with cl.Step(name="Ava is thinking...", show_input=False):

        async for chunk in graph.astream({
            "messages": [HumanMessage(content=message.content)],
            "user_id": user_id
        }):
            if "messages" in chunk:
                last_msg = chunk["messages"][-1]

                if hasattr(last_msg, "content") and last_msg.content:
                    full_response += last_msg.content
                    await msg.stream_token(last_msg.content)
                    await cl.sleep(0.01)

    msg.content = full_response
    await msg.update()

    # Image handling
    image_match = re.search(r"(https://image\.pollinations\.ai[^\s]+)", full_response)

    if image_match:
        await cl.Image(
            url=image_match.group(1),
            name="Ava's creation"
        ).send()

    # Audio handling
    if full_response.strip().endswith(".mp3"):
        await cl.Audio(
            path=full_response.strip(),
            autoplay=True
        ).send()
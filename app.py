import chainlit as cl
from langchain_core.messages import HumanMessage
from ai_companion.graph.graph import create_graph
import re
import os 

PORT = int(os.environ.get("PORT", 8000))

graph = create_graph()


# 🚀 CHAT START (WELCOME SCREEN)
@cl.on_chat_start
async def start():
    user_id = cl.user_session.get("id")

    if not user_id:
        user_id = str(id(cl.user_session))
        cl.user_session.set("id", user_id)

    await cl.Message(
        content="""
Hey, I'm **Ava** 👋  

I'm your AI companion - I can create images, speak, an remember things about you.

What's on your mind today ?
""",
        author="Ava",
        avatar="https://cdn-icons-png.flaticon.com/512/4712/4712027.png"
    ).send()


# 💬 MAIN CHAT
@cl.on_message
async def main(message: cl.Message):
    user_id = cl.user_session.get("id")

    msg = cl.Message(
        content="",
        author="Ava",
        avatar="public/avatar.png")
    await msg.send()

    full_response = ""

    # 🧠 Thinking indicator
    async with cl.Step(name="Ava is thinking...", show_input=False):

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

    # Final update
    msg.content = full_response
    await msg.update()

    # 🖼️ IMAGE HANDLING
    image_match = re.search(r"(https://image\.pollinations\.ai[^\s]+)", full_response)

    if image_match:
        image_url = image_match.group(1)

        await cl.Image(
            url=image_url,
            name="Ava's creation"
        ).send()

    # 🔊 AUDIO HANDLING
    if full_response.strip().endswith(".mp3"):
        await cl.Audio(
            path=full_response.strip(),
            autoplay=True
        ).send()
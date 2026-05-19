import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from ai_companion.graph.graph import create_graph


async def main():
    graph = create_graph()

    messages = []

    print("Ava is live. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # Add user message
        messages.append(HumanMessage(content=user_input))

        # Call graph
        result = await graph.ainvoke({
            "messages": [HumanMessage(content=user_input)],
            "user_id" : "manya"
        })

        # Get AI response
        ai_msg = result["messages"][-1].content
        print("Ava:", ai_msg)

        # Update memory (IMPORTANT)
        messages = result["messages"]


if __name__ == "__main__":
    asyncio.run(main())
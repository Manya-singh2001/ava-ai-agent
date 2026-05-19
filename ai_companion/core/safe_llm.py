async def safe_ainvoke(model, prompt, fallback="Sorry, something went wrong."):
    try:
        response = await model.ainvoke(prompt)
        return response
    except Exception as e:
        print("LLM Error:", e)
        return type("obj", (object,), {"content": fallback})
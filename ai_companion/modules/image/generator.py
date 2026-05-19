import requests
from langchain_groq import ChatGroq
from ai_companion.settings import settings
from ai_companion.core.prompts import (
    IMAGE_SCENARIO_PROMPT,
    IMAGE_ENHANCEMENT_PROMPT
)
import json


class ImageGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.SMALL_TEXT_MODEL_NAME,
            api_key=settings.GROQ_API_KEY,
            temperature=0.7
        )

    async def generate(self, chat_history: str):
        #  Scenario creation
        scenario_prompt = IMAGE_SCENARIO_PROMPT.format(
            chat_history=chat_history
        )

        scenario_res = await self.llm.ainvoke(scenario_prompt)

        try:
            data = json.loads(scenario_res.content)
        except Exception:
            return{
                "narrarive": "I tried to visualize something cool, but it got a bit messy 😅",
                "image_url": "https://image.pollinations.ai/prompt/futuristic city"
            }

        narrative = data["narrative"]
        base_prompt = data["image_prompt"]

        # Prompt enhancement
        enhance_prompt = IMAGE_ENHANCEMENT_PROMPT.format(
            prompt=base_prompt
        )

        enhanced = await self.llm.ainvoke(enhance_prompt)
        final_prompt = enhanced.content

        # Image generation (Pollinations)
        url = f"https://image.pollinations.ai/prompt/{final_prompt}"

        return {
            "narrative": narrative,
            "image_url": url
        }
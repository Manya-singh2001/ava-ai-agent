import requests
import urllib.parse


class TextToImage:
    async def generate_image(self, prompt: str) -> bytes:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        # encode prompt for URL
        encoded_prompt = urllib.parse.quote(prompt)

        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Image API failed: {response.text}")

        return response.content
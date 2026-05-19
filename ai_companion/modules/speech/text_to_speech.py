import edge_tts
import asyncio
import uuid
import os


class TextToSpeech:
    def __init__(self):
        self.voice = "en-US-JennyNeural"  # 🔥 best default female voice

    async def generate(self, text: str) -> str:
        """
        Generates audio and saves it to a file.
        Returns file path.
        """

        filename = f"audio_{uuid.uuid4().hex}.mp3"

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice
        )

        await communicate.save(filename)

        return filename
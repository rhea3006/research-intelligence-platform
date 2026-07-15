import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-flash-lite-latest",
        )

    def generate_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text.strip()


# Singleton instance used throughout the project
llm = GeminiService()
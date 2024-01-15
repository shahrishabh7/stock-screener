from typing import Any, Optional
import requests
import os

from openai_completions import OpenAI
from pydantic import BaseModel

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class OpenAIService:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

    async def completion(
        self,
        prompt: str,
        temperature: int = 0,
    ) -> str:
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=data,
            headers=self.headers
        )
        return response.json()

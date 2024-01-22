from typing import Any, Optional
import requests
import os

from openai import OpenAI
from pydantic import BaseModel

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class OpenAIService:
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: str = ''):
        self.client = OpenAI()
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    async def market_analysis_completion(
        self,
        prompt: str,
        temperature: int = 0,
    ) -> str:
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant helping me synthesize market news to evaluate the position of a company."
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

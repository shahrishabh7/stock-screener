from typing import Any, Optional
import requests
import os

from helicone.openai_async import openai
from pydantic import BaseModel

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HELICONE_API_KEY = os.getenv('HELICONE_API_KEY')


class OpenAIService:
    def __init__(self, model: str = "gpt-3.5-turbo-16k", api_key: str = OPENAI_API_KEY):
        self.model = model
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Helicone-Auth": f"Bearer {HELICONE_API_KEY}",
        }

    async def market_analysis_completion(
        self,
        prompt: str,
        temperature: int = 0,
    ) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "You are an assistant helping me synthesize market news to evaluate the position of a company"
            },
                {
                "role": "user",
                "content": prompt
            }],
            max_tokens=512,
            temperature=temperature,
        )
        return response['choices'][0]['message']['content']

    async def competitor_analysis_completion(
        self,
        prompt: str,
        temperature: int = 0,
    ) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "You are an assistant helping me synthesize insights on a company's competitors and how their stock is performing."
            },
                {
                "role": "user",
                "content": prompt
            }],
            max_tokens=512,
            temperature=temperature,
        )
        return response['choices'][0]['message']['content']

    async def filings_analysis_completion(
        self,
        prompt: str,
        temperature: int = 0,
    ) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{
                "role": "system",
                "content": "You are an assistant helping me summarize insights from a section of a company's 10k."
            },
                {
                "role": "user",
                "content": prompt
            }],
            max_tokens=512,
            temperature=temperature,
        )
        return response['choices'][0]['message']['content']

import os
from typing import Optional, Any, Dict
from serpapi import search as GoogleSearch

SERP_API_KEY = os.getenv('SERP_API_KEY')


class SerpService:
    def __init__(self, api_key: Optional[str], engine: str = "google_news"):
        self.url = "https://serpapi.com/search"
        self.api_key = SERP_API_KEY
        self.params = {
            "api_key": {self.api_key},
            "gl": "us",
        }
        if engine:
            self.params["engine"] = engine

    def search(self, query: str) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("No API key provided")

        self.params["q"] = query
        search = GoogleSearch(self.params)
        results = search.as_dict()
        return results

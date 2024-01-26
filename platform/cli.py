import os
import time
import asyncio
import json
from typing import Optional
from pydantic import BaseModel

import requests
import pandas as pd
from screener import Screener
from beautifulsoup import Article, BeautifulSoupService
from serp import SerpService
from openai_completions import OpenAIService


async def main():
    while True:
        user_input = input("Enter company ticker: ")
        if user_input.lower() == 'exit':
            break

        screener = Screener(ticker=user_input)
        # filings_analysis = await screener.analyze_10k()
        # market_analysis = await screener.synthesize_market_news()
        # competitor_analysis = await screener.analyze_competitors()
        print("Filings Analysis")
        print("---------------")
        print("filings_analysis")

        print("Market Analysis")
        print("---------------")
        print("market_analysis")

        print("Competitor Analysis")
        print("---------------")
        print("competitor_analysis")


if __name__ == '__main__':
    asyncio.run(main())

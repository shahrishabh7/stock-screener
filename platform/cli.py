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
    screener = Screener()
    while True:
        user_input = input("Enter company ticker: ")
        if user_input.lower() == 'exit':
            break

        # filings_analysis = await screener.analyze_10k(user_input)
        # market_analysis = await screener.synthesize_market_news(user_input)
        competitor_analysis = await screener.analyze_competitors(user_input)
        print(competitor_analysis)

        print('Company Analysis:')


if __name__ == '__main__':
    asyncio.run(main())

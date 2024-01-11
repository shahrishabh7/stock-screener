import os
import time
import asyncio
import json


def show_json(obj):
    print(json.loads(obj.model_dump_json()))


def analyze_10k(company_name):
    pass


def synthesize_market_news(company_name):
    pass


def analyze_competitors(company_name):
    pass


async def main():
    while True:
        user_input = input("Enter company name: ")
        if user_input.lower() == 'exit':
            break

        filings_analysis = analyze_10k(user_input)
        market_analysis = synthesize_market_news(user_input)
        competitor_analysis = analyze_competitors(user_input)

        print('Company Analysis:')


if __name__ == '__main__':
    asyncio.run(main())

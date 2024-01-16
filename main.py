import os
import time
import asyncio
import json

import requests
import pandas as pd

from beautifulsoup import BeautifulSoupService
from serp import SerpService
from openai_completions import OpenAIService


class Screener:

    def __init__(self):
        self.serper = SerpService('')
        self.ticker_to_cik = {}

        # create request header
        self.headers = {'User-Agent': "rohith.mandavilli@gmail.com"}

        # get all companies data
        company_tickers = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=self.headers
        )
        # review response / keys
        company_ticker_data = company_tickers.json()
        for key in company_ticker_data.keys():
            company = company_ticker_data[key]
            cik_str = str(company['cik_str'])
            cik_len = len(cik_str)
            leading_zeros = (10 - cik_len) * "0"
            self.ticker_to_cik[company['ticker']] = leading_zeros + str(cik_str)

        print("...retrieved company data...")

    async def analyze_10k(self, company_ticker):
        """
        get SEC filings from EDGAR, start with 10k
        """

        # get company specific filing metadata
        assert company_ticker in self.ticker_to_cik, "TICKER DOESNT EXIST"
        cik = self.ticker_to_cik[company_ticker]
        filing_metadata_response = requests.get(
            f'https://data.sec.gov/submissions/CIK{cik}.json',
            headers=self.headers
        )
        filings = filing_metadata_response.json()

        # review json
        print(filings.keys())
        print(filings['filings'].keys())
        print(filings['filings']['recent'].keys())
        # dict_keys(['cik', 'entityType', 'sic', 'sicDescription', 'insiderTransactionForOwnerExists', 'insiderTransactionForIssuerExists', 'name', 'tickers', 'exchanges', 'ein', 'description', 'website', 'investorWebsite', 'category', 'fiscalYearEnd', 'stateOfIncorporation', 'stateOfIncorporationDescription', 'addresses', 'phone', 'flags', 'formerNames', 'filings'])
        # dict_keys(['recent', 'files'])
        # dict_keys(['accessionNumber', 'filingDate', 'reportDate', 'acceptanceDateTime', 'act', 'form', 'fileNumber', 'filmNumber', 'items', 'size', 'isXBRL', 'isInlineXBRL', 'primaryDocument', 'primaryDocDescription'])
        forms = pd.DataFrame.from_dict(filings['filings']['recent'])
        most_recent_10k = None
        for index, row in forms.iterrows():
            if row['form'] == "10-K":
                print(row)
                most_recent_10k = row
                break

        assert most_recent_10k is not None
        # https://www.sec.gov/Archives/edgar/data/1321655/000132165523000011/pltr-20221231.htm
        print(most_recent_10k)
        sec_link_10k = f'https://www.sec.gov/Archives/edgar/data/{cik}/{most_recent_10k["accessionNumber"].replace("-", "")}/{most_recent_10k["primaryDocument"]}'
        print(sec_link_10k)
        
        # 
        bs = BeautifulSoupService(sec_link_10k)
        await bs.generate_pdf()
        # print(sec_10k_page_content)
        open_ai = OpenAIService()
        prompt = ""
        # open_ai_resp = await open_ai.completion(prompt)

    def synthesize_market_news(self, company_ticker):
        news = self.serper.search(f'"company_name"' + " market news")
        return news

    def analyze_competitors(self, company_ticker):
        pass


async def main():
    screener = Screener()
    while True:
        user_input = input("Enter company ticker: ")
        if user_input.lower() == 'exit':
            break

        filings_analysis = await screener.analyze_10k(user_input)
        market_analysis = screener.synthesize_market_news(user_input)
        competitor_analysis = screener.analyze_competitors(user_input)

        print('Company Analysis:')


if __name__ == '__main__':
    asyncio.run(main())

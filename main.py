import os
import time
import asyncio
import json

import requests
import pandas as pd


class Screener:
    
    
    def __init__(self):
        self.ticker_to_cik = {}

        # create request header
        self.headers = {'User-Agent': "email@address.com"}

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


    def analyze_10k(self, company_ticker):
        """
        get SEC filings from EDGAR, start with 10k
        """
        
        # get company specific filing metadata
        assert company_ticker in self.ticker_to_cik, "TICKER DOESNT EXIST"
        cik = self.ticker_to_cik[company_ticker]
        print(cik)
        filing_metadata = requests.get(
            f'https://data.sec.gov/submissions/CIK{cik}.json',
            headers=self.headers
        )
        filings = filing_metadata.json()

        
        # review json 
        print(filings.keys())
        print(filings['filings'].keys())
        print(filings['filings']['recent'].keys())

        # dictionary to dataframe

    def synthesize_market_news(self, company_name):
        pass


    def analyze_competitors(self, company_name):
        pass


async def main():
    screener = Screener()
    while True:
        user_input = input("Enter company ticker: ")
        if user_input.lower() == 'exit':
            break
    
        filings_analysis = screener.analyze_10k(user_input)
        market_analysis = screener.synthesize_market_news(user_input)
        competitor_analysis = screener.analyze_competitors(user_input)

        print('Company Analysis:')


if __name__ == '__main__':
    asyncio.run(main())

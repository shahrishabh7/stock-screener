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
        headers = {'User-Agent': "email@address.com"}

        # get all companies data
        company_tickers = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=headers
        )
        # review response / keys
        company_ticker_data = company_tickers.json()
        for key in company_ticker_data.keys():
            company = company_ticker_data[key]
            self.ticker_to_cik[company['ticker']] = company['cik_str']
        
        print("...retrieved company data...")


    def analyze_10k(company_ticker):
        """
        get SEC filings from EDGAR, start with 10k
        """
        
        # get company specific filing metadata
        # filingMetadata = requests.get(
        #     f'https://data.sec.gov/submissions/CIK{cik}.json',
        #     headers=headers
        # )

        # # review json 
        # print(filingMetadata.json().keys())
        # filingMetadata.json()['filings']
        # filingMetadata.json()['filings'].keys()
        # filingMetadata.json()['filings']['recent']
        # filingMetadata.json()['filings']['recent'].keys()

        # # dictionary to dataframe
        # allForms = pd.DataFrame.from_dict(
        #     filingMetadata.json()['filings']['recent']
        # )



    def synthesize_market_news(company_name):
        pass


    def analyze_competitors(company_name):
        pass


async def main():
    while True:
        user_input = input("Enter company ticker: ")
        if user_input.lower() == 'exit':
            break
    
        screener = Screener()

        filings_analysis = screener.analyze_10k(user_input)
        market_analysis = screener.synthesize_market_news(user_input)
        competitor_analysis = screener.analyze_competitors(user_input)

        print('Company Analysis:')


if __name__ == '__main__':
    asyncio.run(main())

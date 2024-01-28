from typing import Dict, Optional
import pandas as pd
from pydantic import BaseModel
import requests
from beautifulsoup import Article, BeautifulSoupService
from openai_completions import OpenAIService
from serp import SerpService

from transformers import AutoModelForCausalLM, AutoTokenizer


class Screener:

    def __init__(self, ticker: str):
        self.serper = SerpService(
            api_key='')
        self.ticker_to_cik = {}
        self.ticker = ticker

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
            self.ticker_to_cik[company['ticker']
                               ] = leading_zeros + str(cik_str)

        assert self.ticker in self.ticker_to_cik, "TICKER DOESNT EXIST"
        print("...retrieved company data...")

    async def analyze_all(self) -> Dict[str, str]:
        # filings_analysis = await self.analyze_10k()
        market_analysis = await self.synthesize_market_news()
        competitor_analysis = await self.analyze_competitors()

        return {
            "filings_analysis": 'filings_analysis',
            "market_analysis": market_analysis,
            "competitor_analysis": competitor_analysis
        }

    async def analyze_10k(self):
        """
        get SEC filings from EDGAR, start with 10k
        """

        # get company specific filing metadata
        cik = self.ticker_to_cik[self.ticker]
        filing_metadata_response = requests.get(
            f'https://data.sec.gov/submissions/CIK{cik}.json',
            headers=self.headers
        )
        filings = filing_metadata_response.json()

        forms = pd.DataFrame.from_dict(filings['filings']['recent'])
        most_recent_10k = None
        for index, row in forms.iterrows():
            if row['form'] == "10-K":
                print(row)
                most_recent_10k = row
                break

        assert most_recent_10k is not None
        sec_link_10k = f'https://www.sec.gov/Archives/edgar/data/{cik}/{most_recent_10k["accessionNumber"].replace("-", "")}/{most_recent_10k["primaryDocument"]}'
        print(sec_link_10k)

        bs = BeautifulSoupService(sec_link_10k)
        sec_filing_text = await bs.get_text_from_sec_html()

        mgmt_disc_index = sec_filing_text.index(
            "ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS")
        fin_statements_index = sec_filing_text.index(
            "ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA")

        filtered_sec_content = sec_filing_text[mgmt_disc_index: fin_statements_index]
        open_ai = OpenAIService()
        prompt = f"Please summarize this piece of filtered content from {self.ticker} most recent 10K filing:\n\n ************** \n\n {filtered_sec_content} \n*********\n\n"

        filings_analysis = await open_ai.filings_analysis_completion(prompt)
        return filings_analysis

    async def synthesize_market_news(self):
        articles = []
        article_strings = []

        news_response = self.serper.search(
            f'"{self.ticker}"' + " market news")

        for result in news_response['news_results'][:4]:
            if 'stories' in result:
                for story in result['stories']:
                    articles.append(Article(
                        title=story['title'],
                        link=story['link'],
                        source=story['source'],
                        date=story['date']
                    ))
            else:
                articles.append(Article(
                    title=result['title'],
                    link=result['link'],
                    source=result['source'],
                    date=result['date']
                ))

        for article in articles:
            bs_scraper = BeautifulSoupService(article.link)
            article.page_content = await bs_scraper.get_article_from_html()
            article_strings.append(bs_scraper.stringify_article(article))

        open_ai = OpenAIService()
        prompt = "Here are the articles:\n\n" + "\n\n".join(article_strings)
        news_analysis = await open_ai.market_analysis_completion(prompt)
        return news_analysis

    async def analyze_competitors(self):
        articles = []
        article_strings = []

        news_response = self.serper.search(
            f'"{self.ticker}"' + " competitors news")
        for result in news_response['news_results'][:2]:
            articles.append(Article(
                title=result['title'],
                link=result['link'],
                source=result['source'],
                date=result['date']
            ))

        for article in articles:
            bs_scraper = BeautifulSoupService(article.link)
            article.page_content = await bs_scraper.get_article_from_html()
            article_strings.append(bs_scraper.stringify_article(article))

        open_ai = OpenAIService()
        prompt = f"Based on articles on {self.ticker} below, extract and highlights insights on the competitors and their relative performance:\n\n" + \
            "\n\n".join(article_strings)
        competitor_analysis = await open_ai.competitor_analysis_completion(prompt)
        return competitor_analysis

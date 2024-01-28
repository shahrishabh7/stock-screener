from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from screener import Screener

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CompanyInformation(BaseModel):
    ticker: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ticker")
async def execute_analysis(req_body: CompanyInformation) -> Dict[str, str]:
    screener = Screener(ticker=req_body.ticker)
    return await screener.analyze_all()


@app.post("/mock/ticker")
async def mock_execute_analysis(req_body: CompanyInformation) -> Dict[str, str]:
    filings_analysis = "asfdasf"
    market_analysis = "Based on the articles, here is a summary of the market news regarding Netflix: 1. Netflix reported strong fourth-quarter results, exceeding Wall Street's revenue expectations and showing strong user growth. The company added 13.1 million net subscribers, well above expectations of 8.8 million. 2. The company's revenue growth outlook for the next year is robust, with a 16% increase expected year-on-year. Netflix also raised its full-year operating margin guidance and provided EPS guidance above expectations. 3. The market reacted positively to Netflix's results, with the stock jumping 7.9% and reaching a two-year high. Analysts upgraded the stock's rating and raised the price target. 4. The company's introduction of a subscription tier supported by advertising and cracking down on password sharing contributed to its impressive user growth. Netflix ended 2023 with 260 million paid memberships, up nearly 30 million from the previous year. 5. Netflix's profitability also improved, with a full-year operating margin of 21% in 2023 and a surge in free cash flow. Overall, the market sentiment towards Netflix is positive, with the company demonstrating strong growth and profitability. The stock's performance reflects investor confidence in its future prospects."
    competitor_analysis = "Insights on Competitors and Relative Performance: 1. Netflix Inc dominates the streaming landscape with over 260 million global subscribers, giving it the largest subscriber base in the entertainment industry. 2. The introduction of ad-supported subscription plans by Netflix opens up new revenue streams and allows the company to tap into the lucrative advertising market. 3. Netflix faces intense competition and rapid industry changes, which present significant challenges to its market dominance. 4. Strategic partnerships and technological advancements are crucial for Netflix's future growth and to maintain its competitive edge. 5. Netflix's content innovation and brand equity have established it as a cultural phenomenon, with its original programming becoming a significant part of the global entertainment conversation. 6. Content acquisition costs are a primary weakness for Netflix, as the company invests heavily in original and exclusive content, impacting its profitability. 7. Netflix's business model is heavily reliant on subscriber growth, making it vulnerable to factors such as pricing changes, content appeal, and increased competition. 8. The recent expansion into advertising presents a significant opportunity for Netflix to diversify its revenue streams and enhance its financial stability. 9. Netflix is well-positioned to leverage technological advancements, such as generative artificial intelligence, to enhance its service offerings and user experience. 10. The streaming industry is characterized by intense competition, with traditional media companies, new entrants, and alternative entertainment options posing threats to Netflix's market share. 11. Netflix operates in a complex regulatory environment, and effective management of regulatory and legal risks is crucial for its continued success. Relative Performance: - Netflix's stock jumped nearly 11% after reporting adding 13.1 million subscribers during the fourth quarter, exceeding Wall Street's expectations. - The company's revenue for the quarter was $8.83 billion, higher than the expected $8.72 billion. - Netflix's total memberships reached 260.8 million, a new record for the service. - The company increased its 2024 full-year operating margin forecast to 24% and projects higher earnings per share for the fiscal first quarter of 2024. - Netflix is focused on improving profits and investing in its content slate, while its competitors are cutting back on content spend. - The company is expanding its advertising-based plan and aims to make its ad tier more attractive to advertisers. - Netflix sees advertising as a significant long-term revenue potential and is optimistic about its growth in this area."

    return {
        "filings_analysis": filings_analysis,
        "market_analysis": market_analysis,
        "competitor_analysis": competitor_analysis
    }

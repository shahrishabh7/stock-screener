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

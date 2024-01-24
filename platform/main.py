from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CompanyInformation(BaseModel):
    ticker: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ticker")
def execute_analysis(req_body: CompanyInformation):
    return {"ticker": req_body.ticker}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
def execute_analysis(req_body: CompanyInformation):
    return {"ticker": req_body.ticker}

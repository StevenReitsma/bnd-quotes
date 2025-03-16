import requests, json
from datetime import datetime, date
from fastapi import FastAPI, Response, status, HTTPException
from starlette.responses import RedirectResponse
from typing import Optional, List
from cachetools import TTLCache

from models import Quote


app = FastAPI(
    title="BND Quotes",
    description="This project aims to deliver quotes from BrandNewDay.nl funds in a structured manner, with support for PortfolioPerformance.",
    version="1.1.0",
)


# Create caches
fund_name_cache = TTLCache(maxsize=128, ttl=10800)  # 3 hours
quote_cache = TTLCache(maxsize=1024, ttl=10800)  # 3 hours


@app.get(
    "/quotes_by_id/{fundId}",
    response_model=List[Quote],
    summary="Get quotes by fund ID",
    description="This endpoint returns the quotes of the given fund ID of the past 60 days. Use the `/funds` endpoint to get a list of all fund IDs.",
)
async def get_quote_by_id(fundId: int):
    funds = await list_funds()

    if fundId not in funds.values():
        raise HTTPException(status_code=404, detail="Unknown fund ID")

    # Create a hash of the request for caching purposes
    hashId = str(fundId)

    if hashId in quote_cache:
        # Result is cached, return it
        return quote_cache[hashId]

    response = requests.get(
        url=f"https://devrobotapi.azurewebsites.net/roboadvisor/v1/fundrates?id={fundId}",
    )
    bnd_json = response.json()["rates"]

    quote_cache[hashId] = [
        {
            "Date": datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S"),
            "Close": x["nav"],
            "Ask": x["askPrice"],
            "Bid": x["bidPrice"],
        }
        for x in bnd_json
    ]

    return quote_cache[hashId]


@app.get(
    "/quotes/{fundName}",
    response_model=List[Quote],
    summary="Get quotes by fund name",
    description="This endpoint returns the quotes of the given fund name of the past 60 days. Use the `/funds` endpoint to get a list of all fund names.",
)
async def get_quote_by_name(fundName: str):
    funds = await list_funds()

    if fundName not in funds:
        raise HTTPException(status_code=404, detail="Unknown fund name")

    fundId = funds[fundName]
    return await get_quote_by_id(fundId)


@app.get(
    "/funds",
    response_model=dict,
    summary="Get funds",
    description="This endpoint returns all the available fund names and IDs.",
)
async def list_funds():
    if len(fund_name_cache) == 0:
        await fill_fund_name_cache()
    return fund_name_cache


@app.get(
    "/",
    include_in_schema=False,
)
async def index(response: Response):
    response = RedirectResponse(url='https://github.com/StevenReitsma/bnd-quotes', status_code=303)
    return response


async def fill_fund_name_cache():
    response = requests.get(url="https://devrobotapi.azurewebsites.net/roboadvisor/v1/funds")
    bnd_json = response.json()["data"]

    fund_name_cache.clear()

    for x in bnd_json:
        fund_name_cache[str.lower(x["name"]).replace(" ", "-")] = x["id"]

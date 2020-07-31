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
    version="1.0.0",
)


# Create caches
fund_name_cache = TTLCache(maxsize=128, ttl=3600)
quote_cache = TTLCache(maxsize=1024, ttl=3600)


@app.get(
    "/quotes_by_id/{fundId}",
    response_model=List[Quote],
    summary="Get quotes by fund ID",
    description="This endpoint returns the quotes of the given fund ID of the past 60 days. Use the `page` argument to get quotes further into the past. Use the `/funds` endpoint to get a list of all fund IDs.",
)
async def get_quote_by_id(fundId: int, page: Optional[int] = 1):
    if page < 1:
        raise HTTPException(status_code=400, detail="Invalid page")

    funds = await list_funds()

    if fundId not in funds.values():
        raise HTTPException(status_code=404, detail="Unknown fund ID")

    # Create a hash of the request for caching purposes
    hashId = str(fundId) + "|" + str(page)

    if hashId in quote_cache:
        # Result is cached, return it
        return quote_cache[hashId]

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    data = {
        "page": page,
        "pageSize": 60,
        "fundId": fundId,
        "startDate": "01-01-2010",
        "endDate": date.today().strftime("%d-%m-%Y"),
    }

    response = requests.post(
        url="https://secure.brandnewday.nl/service/navvaluesforfund",
        headers=headers,
        data=data,
    )
    bnd_json = response.json()

    quote_cache[hashId] = [
        {
            "Date": datetime.utcfromtimestamp(
                int(x["RateDate"].replace("/Date(", "").replace(")/", "")) / 1000
            ),
            "Close": x["LastRate"],
            "Ask": x["AskRate"],
            "Bid": x["BidRate"],
        }
        for x in bnd_json["Data"]
    ]

    return quote_cache[hashId]


@app.get(
    "/quotes/{fundName}",
    response_model=List[Quote],
    summary="Get quotes by fund name",
    description="This endpoint returns the quotes of the given fund name of the past 60 days. Use the `page` argument to get quotes further into the past. Use the `/funds` endpoint to get a list of all fund names.",
)
async def get_quote_by_name(fundName: str, page: Optional[int] = 1):
    funds = await list_funds()

    if fundName not in funds:
        raise HTTPException(status_code=404, detail="Unknown fund name")

    fundId = funds[fundName]
    return await get_quote_by_id(fundId, page)


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
    response = requests.get(url="https://secure.brandnewday.nl/service/getfunds")
    bnd_json = json.loads(response.json()["Message"])

    fund_name_cache.clear()

    for x in bnd_json:
        fund_name_cache[str.lower(x["Value"]).replace(" ", "-")] = x["Key"]

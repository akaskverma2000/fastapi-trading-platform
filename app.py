import datetime as dt
import enum

from typing import Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI, Form, Query

from starlette.responses import RedirectResponse
from fastapi_pagination import Page, add_pagination, paginate

import uvicorn

from typing import List

# Model
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")

    price: float = Field(description="The price of the Trade.")

    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")

    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")

    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")

    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")

    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")

    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")

    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")

    trader: str = Field(description="The name of the Trader")

# Hard Coded Database
raw_trade = [
    {
    "assetClass": "Bond",
    "counterparty": "Hastiin",
    "instrumentId": "GHJD",
    "instrumentName": "Debentures",
    "tradeDateTime": "2024-07-04 00:02:35.520788",
    "tradeDetails": {
        "buySellIndicator": "BUY",
        "price": 9.36,
        "quantity": 42
    },
    "tradeId": "8c8f9d65-ef45-43cc-9253-badac16bdba9",
    "trader": "Akash"
    },
    {
        "assetClass": "Bond",
        "counterparty": "Masamba",
        "instrumentId": "TSWQ",
        "instrumentName": "Debentures",
        "tradeDateTime": "2021-02-03 00:03:35.520788",
        "tradeDetails": {
            "buySellIndicator": "SELL",
            "price": 1.36,
            "quantity": 32
        },
        "tradeId": "f0aed2de-d4d2-4213-bed1-60bd6fb1d2b0",
        "trader": "Otar"
    },
    {
        "assetClass": "Equity",
        "counterparty": "Fyokla",
        "instrumentId": "TSEW",
        "instrumentName": "Preference Shares",
        "tradeDateTime": "2022-12-03 00:03:35.520788",
        "tradeDetails": {
            "buySellIndicator": "BUY",
            "price": 2.36,
            "quantity": 12
        },
        "tradeId": "8ae396c4-94e3-400b-b44a-ebfc06ef131c",
        "trader": "Koba"
    },
    {
        "assetClass": "Equity",
        "counterparty": "Isokrates",
        "instrumentId": "DAWD",
        "instrumentName": "Mutual Funds",
        "tradeDateTime": "2023-10-03 00:06:35.520788",
        "tradeDetails": {
            "buySellIndicator": "SELL",
            "price": 5.36,
            "quantity": 22
        },
        "tradeId": "a3fff395-d13f-4faf-80d6-71b291d43cf0",
        "trader": "Jaycee"
    }
]

app = FastAPI()

class sortChoice(str, enum.Enum):
    asc = "asc"
    desc = "desc"

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

# 1 Fetch a list of trades
@app.get("/trades/", status_code=200, response_model=Page[Trade])
def fetch_all_trades(*,assetClassSort: sortChoice = Query(None), counterpartySort: sortChoice = Query(None), instrumentIdSort: sortChoice = Query(None), instrumentNameSort: sortChoice = Query(None), tradeDateTimeSort: sortChoice = Query(None), buySellIndicatorSort: sortChoice = Query(None), priceSort: sortChoice = Query(None), quantitySort: sortChoice = Query(None),tradeIdSort: sortChoice = Query(None), traderSort: sortChoice = Query(None)) -> list:
    """
    Fetch a list of trades
    """
    res = raw_trade
    if assetClassSort == "asc":
        res = sorted(raw_trade, key=lambda trade: trade['assetClass']) 
    
    if assetClassSort == "desc":
        res = sorted(raw_trade, key=lambda trade: trade['assetClass'], reverse=True)
    
    if counterpartySort == "asc":
        res = sorted(res, key=lambda trade: trade['counterparty']) 
    
    if counterpartySort == "desc":
        res = sorted(res, key=lambda trade: trade['counterparty'], reverse=True)

    if instrumentIdSort == "asc":
        res = sorted(res, key=lambda trade: trade['instrumentId']) 
    
    if instrumentIdSort == "desc":
        res = sorted(res, key=lambda trade: trade['instrumentId'], reverse=True)
    
    if instrumentNameSort == "asc":
        res = sorted(res, key=lambda trade: trade['instrumentName']) 
    
    if instrumentNameSort == "desc":
        res = sorted(res, key=lambda trade: trade['instrumentName'], reverse=True)

    if tradeDateTimeSort == "asc":
        res = sorted(res, key=lambda trade: trade['tradeDateTime']) 
    
    if tradeDateTimeSort == "desc":
        res = sorted(res, key=lambda trade: trade['tradeDateTime'], reverse=True)

    if buySellIndicatorSort == "asc":
        res = sorted(res, key=lambda trade: trade['tradeDetails']['buySellIndicator']) 
    
    if buySellIndicatorSort == "desc":
        res = sorted(res, key=lambda trade: trade['tradeDetails']['buySellIndicator'], reverse=True)
    
    if quantitySort == "asc":
        res = sorted(res, key=lambda trade: trade['tradeDetails']['quantity']) 
    
    if quantitySort == "desc":
        res = sorted(res, key=lambda trade: trade['tradeDetails']['quantity'], reverse=True)
    
    if traderSort == "asc":
        res = sorted(res, key=lambda trade: trade['trader']) 
    
    if traderSort == "desc":
        res = sorted(res, key=lambda trade: trade['trader'], reverse=True)

    if tradeIdSort == "asc":
        res = sorted(res, key=lambda trade: trade['tradeId']) 
    
    if tradeIdSort == "desc":
        res = sorted(res, key=lambda trade: trade['tradeId'], reverse=True)
    
    if priceSort == "asc":
        res = sorted(res, key=lambda trade: trade['tradeDetails']['price']) 
    
    if priceSort == "desc":
        res = sorted(res, key=lambda trade: trade['tradeDetails']['price'], reverse=True)

    return paginate(res)

# 2 Fetch a trade by ID
@app.get("/trades/{trade_id}", status_code=200, response_model=Trade)
def fetch_trade_by(*, trade_id: str) -> dict:
    """
    Fetch a trade by ID
    """

    result = [trade for trade in raw_trade if trade["tradeId"] == trade_id]
    if result:
        return result[0]

# 3 Fetch a list of trades will searching for trades through counterparty, instrumentId, instrumentName and trader.
@app.get("/trade", status_code=200, response_model=Page[Trade])
def search_trade(*, search: str = Query(None)) -> list:
    """
    Fetch a list of trades will searching for trades through counterparty, instrumentId, instrumentName and trader.
    """
    results = []
    for trade in raw_trade:
        if search.lower() in trade["counterparty"].lower() or search.lower() in trade["instrumentId"].lower() or search.lower() in trade["instrumentName"].lower() or search.lower() in trade["trader"].lower():
            results.append(trade)

    return paginate(results)

# 4 Fetch a list of trades will searching for trades through assetClass, end, maxPrice, minPrice, start and tradeType.
@app.get("/trades", status_code=200, response_model=Page[Trade])
def advance_search_trade(*, assetClass: str = Query(None), maxPrice: float = Query(None), minPrice: float = Query(None), tradeType: str = Query(None), end: dt.datetime = Query(None), start: dt.datetime = Query(None)) -> list:
    """
    Fetch a list of trades will searching for trades through assetClass, end, maxPrice, minPrice, start and tradeType.
    """
    results = []
    for trade in raw_trade:
        flagAssetClass = True
        flagTradeType = True
        flagMinPrice = True
        flagMaxPrice = True
        flagStart = True
        flagEnd = True

        if assetClass != None:
            flagAssetClass = False
        if tradeType != None:
            flagTradeType = False
        if minPrice != None:
            flagMinPrice = False
        if maxPrice != None:
            flagMaxPrice = False
        if start != None:
            flagStart = False
        if end != None:
            flagEnd = False

        if assetClass != None:
            if assetClass.lower() in trade["assetClass"].lower():
                flagAssetClass = True
        if tradeType != None:
            if tradeType.lower() in trade["tradeDetails"]["buySellIndicator"].lower():
                flagTradeType = True

        if minPrice != None:
            if trade["tradeDetails"]["price"] >= minPrice:
                flagMinPrice = True
        
        if maxPrice != None:
            if maxPrice != None:
                if trade["tradeDetails"]["price"] <= maxPrice:
                    flagMaxPrice = True

        if start != None:
            if str(start) >= trade["tradeDateTime"]:
                flagStart = True
        if end != None:
            if str(end) <= trade["tradeDateTime"]:
                flagEnd = True

        if flagAssetClass and flagTradeType and flagMinPrice and flagMaxPrice and flagStart and flagEnd:
            results.append(trade)

    return paginate(results)

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("app:app", port=9000, reload=True)
    
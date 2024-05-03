from fastapi import APIRouter, Query
from fastapi_pagination import Page, add_pagination, paginate
from app.models.trade import Trade
from typing import List
from utils.database import raw_trade

router = APIRouter()

# 1 Fetch a list of trades


@app.get("/trades/", status_code=200, response_model=Page[Trade])
def fetch_all_trades(*, assetClassSort: sortChoice = Query(None), counterpartySort: sortChoice = Query(None), instrumentIdSort: sortChoice = Query(None), instrumentNameSort: sortChoice = Query(None), tradeDateTimeSort: sortChoice = Query(None), buySellIndicatorSort: sortChoice = Query(None), priceSort: sortChoice = Query(None), quantitySort: sortChoice = Query(None), tradeIdSort: sortChoice = Query(None), traderSort: sortChoice = Query(None)) -> list:
    """
    Fetch a list of trades
    """
    res = raw_trade
    if assetClassSort == "asc":
        res = sorted(raw_trade, key=lambda trade: trade['assetClass'])

    if assetClassSort == "desc":
        res = sorted(
            raw_trade, key=lambda trade: trade['assetClass'], reverse=True)

    if counterpartySort == "asc":
        res = sorted(res, key=lambda trade: trade['counterparty'])

    if counterpartySort == "desc":
        res = sorted(
            res, key=lambda trade: trade['counterparty'], reverse=True)

    if instrumentIdSort == "asc":
        res = sorted(res, key=lambda trade: trade['instrumentId'])

    if instrumentIdSort == "desc":
        res = sorted(
            res, key=lambda trade: trade['instrumentId'], reverse=True)

    if instrumentNameSort == "asc":
        res = sorted(res, key=lambda trade: trade['instrumentName'])

    if instrumentNameSort == "desc":
        res = sorted(
            res, key=lambda trade: trade['instrumentName'], reverse=True)

    if tradeDateTimeSort == "asc":
        res = sorted(res, key=lambda trade: trade['tradeDateTime'])

    if tradeDateTimeSort == "desc":
        res = sorted(
            res, key=lambda trade: trade['tradeDateTime'], reverse=True)

    if buySellIndicatorSort == "asc":
        res = sorted(
            res, key=lambda trade: trade['tradeDetails']['buySellIndicator'])

    if buySellIndicatorSort == "desc":
        res = sorted(
            res, key=lambda trade: trade['tradeDetails']['buySellIndicator'], reverse=True)

    if quantitySort == "asc":
        res = sorted(res, key=lambda trade: trade['tradeDetails']['quantity'])

    if quantitySort == "desc":
        res = sorted(
            res, key=lambda trade: trade['tradeDetails']['quantity'], reverse=True)

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
        res = sorted(
            res, key=lambda trade: trade['tradeDetails']['price'], reverse=True)

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


add_pagination(router)

from pydantic import BaseModel, Field
import datetime as dt


class TradeDetails(BaseModel):
    buySellIndicator: str = Field(
        description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: str = Field(alias="assetClass", default=None,
                             description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: str = Field(
        default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(
        alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(
        alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(
        alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(
        alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None,
                          description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

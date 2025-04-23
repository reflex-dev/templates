from typing import Literal, TypedDict, Union


class ChartDataPoint(TypedDict):
    time: str
    price: float


class Option(TypedDict):
    type: Literal["Call", "Put"]
    mark: float
    percent_change_to: float
    delta: float
    oi: int
    volume: int
    iv: float
    low: float
    high: float
    bid: float
    ask: float
    strike: float
    gamma: float


class Order(TypedDict):
    symbol: str
    status: Literal["Sending", "Working", "Filled", "Canceled"]
    side: Literal["Buy", "Sell"]
    type: Literal["Market", "Limit", "Stop market"]
    qty: int
    total_cost: float


class Position(TypedDict):
    symbol: str
    qty: float
    mkt_val: float
    day_return: float
    day_percent: float
    total_ret: float
    mark: float
    avg_cost: float
    bid: float
    ask: float
    delta: float
    gamma: float
    theta: float
    iv: Union[float, None]
    type: Literal["Equities", "Options"]
    dte: Union[int, str]


class StockInfo(TypedDict):
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: str
    open: float
    high: float
    low: float
    close: float

from typing import List, TypedDict


class NetWorthDataPoint(TypedDict):
    date: str
    value: float


class SparklinePoint(TypedDict):
    value: float


class AccountDetail(TypedDict):
    id: str
    name: str
    type: str
    balance: float
    last_updated: str
    logo_url: str
    sparkline_data: List[SparklinePoint]


class AccountCategory(TypedDict):
    category_name: str
    total_balance: float
    one_month_change: float
    one_month_change_percent: float
    accounts: List[AccountDetail]
    is_open: bool


class AssetLiabilitySummaryItem(TypedDict):
    name: str
    value: float
    color: str

from typing import List, TypedDict


class NavItem(TypedDict):
    name: str
    icon: str
    active: bool


class ShortcutItem(TypedDict):
    name: str
    icon: str


class BillingStat(TypedDict):
    label: str
    value: str
    total: str
    percentage: float


class CostItem(TypedDict):
    label: str
    value: str
    value_num: float
    percentage: float
    color: str


class ChartDataPoint(TypedDict):
    date: str
    value1: int
    value2: int


class OverviewMetric(TypedDict):
    id: str
    title: str
    change: str
    change_color: str
    value: str
    previous_value: str
    chart_data: List[ChartDataPoint]

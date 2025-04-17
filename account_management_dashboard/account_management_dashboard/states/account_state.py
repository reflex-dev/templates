import reflex as rx
from typing import TypedDict, List, Dict, Union
import datetime
import random


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


class AccountState(rx.State):
    """Holds the state for the financial dashboard."""

    sidebar_items: List[Dict[str, str]] = [
        {"name": "Dashboard", "icon": "home"},
        {"name": "Accounts", "icon": "credit_card"},
        {"name": "Transactions", "icon": "list"},
        {"name": "Cash Flow", "icon": "trending_up"},
        {"name": "Reports", "icon": "bar_chart"},
        {"name": "Budget", "icon": "pie_chart"},
        {"name": "Recurring", "icon": "repeat"},
        {"name": "Goals", "icon": "target"},
        {"name": "Investments", "icon": "dollar_sign"},
        {"name": "Advice", "icon": "message_circle"},
    ]
    active_page: str = "Accounts"
    user_name: str = "Melanie Smith"
    net_worth: float = 687041.79
    net_worth_change_amount: float = 23542.96
    net_worth_change_percent: float = 3.5
    net_worth_performance_data: List[NetWorthDataPoint] = [
        {"date": "Nov 6", "value": 663000},
        {"date": "Nov 8", "value": 664500},
        {"date": "Nov 10", "value": 666000},
        {"date": "Nov 12", "value": 668000},
        {"date": "Nov 14", "value": 670500},
        {"date": "Nov 16", "value": 671000},
        {"date": "Nov 18", "value": 673000},
        {"date": "Nov 20", "value": 675500},
        {"date": "Nov 22", "value": 678000},
        {"date": "Nov 24", "value": 680000},
        {"date": "Nov 26", "value": 681500},
        {"date": "Nov 28", "value": 683000},
        {"date": "Nov 30", "value": 684500},
        {"date": "Dec 2", "value": 686000},
        {"date": "Dec 4", "value": 687500},
        {"date": "Dec 6", "value": 687041.79},
    ]
    selected_graph_range: str = "1 month"
    graph_ranges: List[str] = [
        "1 month",
        "3 months",
        "6 months",
        "1 year",
        "All time",
    ]
    selected_performance_type: str = "Net worth performance"
    account_categories: List[AccountCategory] = [
        {
            "category_name": "Cash",
            "total_balance": 65342.3,
            "one_month_change": 1826.1,
            "one_month_change_percent": 2.9,
            "is_open": True,
            "accounts": [
                {
                    "id": "citi1",
                    "name": "Melanie's Checking",
                    "type": "Checking",
                    "balance": 15234.75,
                    "last_updated": "16 hours ago",
                    "logo_url": "/citi-logo.png",
                    "sparkline_data": [
                        {"value": 15000},
                        {"value": 15100},
                        {"value": 15050},
                        {"value": 15200},
                        {"value": 15150},
                        {"value": 15234.75},
                    ],
                },
                {
                    "id": "joint1",
                    "name": "Joint Savings",
                    "type": "Savings",
                    "balance": 50107.55,
                    "last_updated": "16 hours ago",
                    "logo_url": "/generic-bank-logo.png",
                    "sparkline_data": [
                        {"value": 50000},
                        {"value": 50050},
                        {"value": 50100},
                        {"value": 50080},
                        {"value": 50107.55},
                    ],
                },
            ],
        },
        {
            "category_name": "Credit Cards",
            "total_balance": 2828.99,
            "one_month_change": -63.03,
            "one_month_change_percent": -2.2,
            "is_open": True,
            "accounts": [
                {
                    "id": "amex1",
                    "name": "Joint Credit Card",
                    "type": "Credit Card",
                    "balance": 2828.99,
                    "last_updated": "16 hours ago",
                    "logo_url": "/amex-logo.png",
                    "sparkline_data": [
                        {"value": 2900},
                        {"value": 2880},
                        {"value": 2850},
                        {"value": 2830},
                        {"value": 2828.99},
                    ],
                }
            ],
        },
        {
            "category_name": "Investments",
            "total_balance": 542301.55,
            "one_month_change": 10287.56,
            "one_month_change_percent": 1.9,
            "is_open": True,
            "accounts": [
                {
                    "id": "401k1",
                    "name": "Jon's 401k",
                    "type": "401k",
                    "balance": 180336.73,
                    "last_updated": "1 day ago",
                    "logo_url": "/generic-invest-logo.png",
                    "sparkline_data": [
                        {"value": 178000},
                        {"value": 179000},
                        {"value": 180000},
                        {"value": 180500},
                        {"value": 180336.73},
                    ],
                }
            ],
        },
    ]
    assets_summary: List[AssetLiabilitySummaryItem] = [
        {
            "name": "Investments",
            "value": 542301.55,
            "color": "bg-purple-500",
        },
        {
            "name": "Real Estate",
            "value": 300625.05,
            "color": "bg-blue-500",
        },
        {
            "name": "Cash",
            "value": 65342.3,
            "color": "bg-green-500",
        },
        {
            "name": "Vehicles",
            "value": 20739.77,
            "color": "bg-orange-500",
        },
    ]
    liabilities_summary: List[AssetLiabilitySummaryItem] = [
        {
            "name": "Loans",
            "value": 239137.89,
            "color": "bg-yellow-500",
        },
        {
            "name": "Credit Cards",
            "value": 2828.99,
            "color": "bg-red-500",
        },
    ]
    summary_view: str = "Totals"

    @rx.var
    def total_assets(self) -> float:
        """Calculate total assets."""
        return sum((item["value"] for item in self.assets_summary))

    @rx.var
    def total_liabilities(self) -> float:
        """Calculate total liabilities."""
        return sum((item["value"] for item in self.liabilities_summary))

    @rx.var
    def asset_percentages(
        self,
    ) -> List[AssetLiabilitySummaryItem]:
        """Calculate asset percentages."""
        total = self.total_assets
        if total == 0:
            return [
                {
                    "name": item["name"],
                    "value": 0.0,
                    "color": item["color"],
                }
                for item in self.assets_summary
            ]
        return [
            {
                "name": item["name"],
                "value": round(item["value"] / total * 100, 1),
                "color": item["color"],
            }
            for item in self.assets_summary
        ]

    @rx.var
    def liability_percentages(
        self,
    ) -> List[AssetLiabilitySummaryItem]:
        """Calculate liability percentages."""
        total = self.total_liabilities
        if total == 0:
            return [
                {
                    "name": item["name"],
                    "value": 0.0,
                    "color": item["color"],
                }
                for item in self.liabilities_summary
            ]
        return [
            {
                "name": item["name"],
                "value": round(item["value"] / total * 100, 1),
                "color": item["color"],
            }
            for item in self.liabilities_summary
        ]

    @rx.event
    def set_active_page(self, page_name: str):
        """Set the currently active page in the sidebar."""
        self.active_page = page_name

    @rx.event
    def toggle_account_category(self, category_index: int):
        """Toggle the open/closed state of an account category."""
        if 0 <= category_index < len(self.account_categories):
            category = self.account_categories[category_index].copy()
            category["is_open"] = not category["is_open"]
            self.account_categories[category_index] = category

    @rx.event
    def set_graph_range(self, value: str):
        """Set the time range for the net worth graph."""
        self.selected_graph_range = value
        print(f"Graph range set to: {value}")

    @rx.event
    def set_summary_view(self, view: str):
        """Set the summary view to Totals or Percent."""
        self.summary_view = view

    @rx.event
    def refresh_all(self):
        """Placeholder for refreshing all account data."""
        print("Refreshing all data...")
        self.net_worth += random.uniform(-500, 500)
        self.net_worth_change_amount += random.uniform(-100, 100)
        if self.net_worth > 0:
            current_change = self.net_worth_change_amount
            previous_net_worth = self.net_worth - current_change
            self.net_worth_change_percent = round(
                (
                    current_change / previous_net_worth * 100
                    if previous_net_worth != 0
                    else 0
                ),
                1,
            )
        else:
            self.net_worth_change_percent = 0.0
        if self.net_worth_performance_data:
            new_last_point = self.net_worth_performance_data[-1].copy()
            new_last_point["value"] = round(self.net_worth, 2)
            self.net_worth_performance_data[-1] = new_last_point
        yield rx.toast.info("Data refreshed (simulated)")

    @rx.event
    def add_account(self):
        """Placeholder for adding a new account."""
        print("Add account clicked...")
        yield rx.toast.warning("Add Account functionality not implemented yet.")

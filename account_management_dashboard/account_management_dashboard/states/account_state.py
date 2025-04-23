import datetime
import random
from typing import Dict, List, Union

import reflex as rx
from dateutil.relativedelta import relativedelta

from account_management_dashboard.models.models import (
    AccountCategory,
    AssetLiabilitySummaryItem,
    NetWorthDataPoint,
)
from account_management_dashboard.states.data import account_categories_data


def generate_net_worth_data(
    num_points=365,
    start_value=600000,
    trend=200,
    volatility=1500,
) -> List[NetWorthDataPoint]:
    """Generates realistic net worth data points for the last year."""
    data = []
    today = datetime.date.today()
    current_value = start_value
    start_value -= trend * num_points * 0.5
    for i in range(num_points):
        current_date = today - datetime.timedelta(days=num_points - 1 - i)
        date_str = current_date.strftime("%Y-%m-%d")
        daily_change = random.gauss(trend / 365, volatility / 20)
        current_value += daily_change
        if random.random() < 0.02:
            current_value += random.uniform(-5000, 10000)
        current_value = max(0, current_value)
        data.append(
            {
                "date": date_str,
                "value": round(current_value, 2),
            }
        )
    data[-1]["value"] = 687041.79
    return data


INITIAL_NET_WORTH_DATA = generate_net_worth_data()


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
    net_worth: float = INITIAL_NET_WORTH_DATA[-1]["value"]
    net_worth_change_amount: float = 23542.96
    net_worth_change_percent: float = 3.5
    _raw_net_worth_data: List[NetWorthDataPoint] = INITIAL_NET_WORTH_DATA
    selected_graph_range: str = "1 month"
    graph_ranges: List[str] = [
        "1 month",
        "3 months",
        "6 months",
        "1 year",
        "All time",
    ]
    selected_performance_type: str = "Net worth performance"
    account_categories: List[AccountCategory] = account_categories_data
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
    def net_worth_performance_data(
        self,
    ) -> List[Dict[str, Union[str, float]]]:
        """Filters the net worth data based on the selected range and formats for the graph."""
        if not self._raw_net_worth_data:
            return []
        today = datetime.date.today()
        range_map = {
            "1 month": relativedelta(months=1),
            "3 months": relativedelta(months=3),
            "6 months": relativedelta(months=6),
            "1 year": relativedelta(years=1),
        }
        if self.selected_graph_range == "All time":
            start_date_limit = None
        elif self.selected_graph_range in range_map:
            delta = range_map[self.selected_graph_range]
            start_date_limit = today - delta
        else:
            start_date_limit = today - relativedelta(months=1)
        filtered_data = []
        for point in self._raw_net_worth_data:
            date_obj = datetime.datetime.strptime(point["date"], "%Y-%m-%d").date()
            if start_date_limit is None or date_obj >= start_date_limit:
                if (
                    self.selected_graph_range == "1 year"
                    or self.selected_graph_range == "All time"
                ):
                    display_date = date_obj.strftime("%b %Y")
                else:
                    display_date = date_obj.strftime("%b %d")
                sampling_rate = 1
                if self.selected_graph_range == "1 year":
                    sampling_rate = 7
                elif (
                    self.selected_graph_range == "All time"
                    and len(self._raw_net_worth_data) > 30
                ):
                    total_days = (
                        datetime.datetime.strptime(
                            self._raw_net_worth_data[-1]["date"],
                            "%Y-%m-%d",
                        ).date()
                        - datetime.datetime.strptime(
                            self._raw_net_worth_data[0]["date"],
                            "%Y-%m-%d",
                        ).date()
                    ).days
                    sampling_rate = max(1, total_days // 60)
                point_index = self._raw_net_worth_data.index(point)
                if (
                    len(filtered_data) == 0
                    or point_index % sampling_rate == 0
                    or point_index == len(self._raw_net_worth_data) - 1
                ):
                    filtered_data.append(
                        {
                            "date": display_date,
                            "value": point["value"],
                        }
                    )

        if filtered_data and self._raw_net_worth_data:
            last_raw_date = datetime.datetime.strptime(
                self._raw_net_worth_data[-1]["date"],
                "%Y-%m-%d",
            ).date()
            if (
                self.selected_graph_range == "1 year"
                or self.selected_graph_range == "All time"
            ):
                filtered_data[-1]["date"] = last_raw_date.strftime("%b %Y")
            else:
                filtered_data[-1]["date"] = last_raw_date.strftime("%b %d")
            if filtered_data[-1]["value"] != self._raw_net_worth_data[-1]["value"]:
                filtered_data.append(
                    {
                        "date": filtered_data[-1]["date"],
                        "value": self._raw_net_worth_data[-1]["value"],
                    }
                )
        return filtered_data

    @rx.var
    def total_assets(self) -> float:
        """Calculate total assets."""
        return round(
            sum((item["value"] for item in self.assets_summary)),
            2,
        )

    @rx.var
    def total_liabilities(self) -> float:
        """Calculate total liabilities."""
        cc_balance = next(
            (
                cat["total_balance"]
                for cat in self.account_categories
                if cat["category_name"] == "Credit Cards"
            ),
            0,
        )
        other_liabilities = sum(
            (
                item["value"]
                for item in self.liabilities_summary
                if item["name"] != "Credit Cards"
            )
        )
        return round(other_liabilities + abs(cc_balance), 2)

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
        current_liability_summary = []
        for item in self.liabilities_summary:
            if item["name"] == "Credit Cards":
                cc_balance = next(
                    (
                        cat["total_balance"]
                        for cat in self.account_categories
                        if cat["category_name"] == "Credit Cards"
                    ),
                    0,
                )
                current_liability_summary.append({**item, "value": abs(cc_balance)})
            else:
                current_liability_summary.append(item)
        return [
            {
                "name": item["name"],
                "value": round(item["value"] / total * 100, 1),
                "color": item["color"],
            }
            for item in current_liability_summary
            if item["value"] > 0
        ]

    @rx.event
    def set_active_page(self, page_name: str):
        """Set the currently active page in the sidebar."""
        self.active_page = page_name

    @rx.event
    def toggle_account_category(self, category_index: int):
        """Toggle the open/closed state of an account category."""
        if 0 <= category_index < len(self.account_categories):
            new_categories = [dict(cat) for cat in self.account_categories]
            new_categories[category_index]["is_open"] = not new_categories[
                category_index
            ]["is_open"]
            self.account_categories = new_categories

    @rx.event
    def set_graph_range(self, value: str):
        """Set the time range for the net worth graph."""
        if value in self.graph_ranges:
            self.selected_graph_range = value
        else:
            pass

    @rx.event
    def set_summary_view(self, view: str):
        """Set the summary view to Totals or Percent."""
        if view in ["Totals", "Percent"]:
            self.summary_view = view

    @rx.event
    def refresh_all(self):
        """Placeholder for refreshing all account data. Simulates data changes."""
        new_data = generate_net_worth_data()
        self._raw_net_worth_data = new_data
        self.net_worth = new_data[-1]["value"]
        if len(new_data) > 30:
            month_ago_value = new_data[-31]["value"]
            self.net_worth_change_amount = round(self.net_worth - month_ago_value, 2)
            if month_ago_value != 0:
                self.net_worth_change_percent = round(
                    self.net_worth_change_amount / month_ago_value * 100,
                    1,
                )
            else:
                self.net_worth_change_percent = 0.0
        else:
            self.net_worth_change_amount = 0.0
            self.net_worth_change_percent = 0.0
        new_categories = []
        total_assets_val = 0
        total_liabilities_val = 0
        for category_dict in self.account_categories:
            category = category_dict.copy()
            new_accounts = []
            category_balance_change = 0
            category_opening_balance = category["total_balance"]
            for account_dict in category["accounts"]:
                account = account_dict.copy()
                change_factor = random.uniform(0.98, 1.02)
                prev_balance = account["balance"]
                new_balance = round(prev_balance * change_factor, 2)
                account["balance"] = new_balance
                new_sparkline = account["sparkline_data"][-5:] + [
                    {"value": new_balance}
                ]
                account["sparkline_data"] = new_sparkline
                account["last_updated"] = "Just now"
                new_accounts.append(account)
                balance_diff = new_balance - prev_balance
                category_balance_change += balance_diff
            category["accounts"] = new_accounts
            new_category_total_balance = (
                category_opening_balance + category_balance_change
            )
            category["total_balance"] = round(new_category_total_balance, 2)
            category["one_month_change"] = round(
                category["one_month_change"] * random.uniform(0.9, 1.1),
                2,
            )
            prev_month_balance_approx = (
                category["total_balance"] - category["one_month_change"]
            )
            if prev_month_balance_approx != 0:
                category["one_month_change_percent"] = round(
                    category["one_month_change"] / prev_month_balance_approx * 100,
                    1,
                )
            else:
                category["one_month_change_percent"] = 0.0
            if category["category_name"] == "Credit Cards":
                total_liabilities_val += abs(category["total_balance"])
            else:
                total_assets_val += category["total_balance"]
            new_categories.append(category)
        self.account_categories = new_categories
        new_assets_summary = []
        for item in self.assets_summary:
            item_copy = item.copy()
            matching_category = next(
                (
                    cat
                    for cat in new_categories
                    if cat["category_name"] == item_copy["name"]
                ),
                None,
            )
            if matching_category:
                item_copy["value"] = matching_category["total_balance"]
            else:
                item_copy["value"] = round(
                    item_copy["value"] * random.uniform(0.99, 1.01),
                    2,
                )
            new_assets_summary.append(item_copy)
        self.assets_summary = new_assets_summary
        new_liabilities_summary = []
        cc_category = next(
            (cat for cat in new_categories if cat["category_name"] == "Credit Cards"),
            None,
        )
        cc_total = abs(cc_category["total_balance"]) if cc_category else 0
        for item in self.liabilities_summary:
            item_copy = item.copy()
            if item_copy["name"] == "Credit Cards":
                item_copy["value"] = cc_total
            else:
                item_copy["value"] = round(
                    item_copy["value"] * random.uniform(0.995, 1.005),
                    2,
                )
            new_liabilities_summary.append(item_copy)
        self.liabilities_summary = new_liabilities_summary
        yield rx.toast.info("Data refreshed (simulated)")

    @rx.event
    def add_account(self):
        """Placeholder for adding a new account."""
        yield rx.toast.warning("Add Account functionality not implemented yet.")

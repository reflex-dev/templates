import datetime
import random
from typing import Dict, List, Union

import reflex as rx


def generate_chart_data() -> List[Dict[str, Union[str, int]]]:
    data = []
    today = datetime.date.today()
    for i in range(28):
        date = (today - datetime.timedelta(days=27 - i)).strftime("%Y-%m-%d")
        data.append(
            {
                "date": date,
                "past_28_days": random.randint(1000, 5000),
                "prev_28_days": random.randint(500, 4500),
            }
        )
    return data


def generate_medium_data() -> List[Dict[str, Union[str, int]]]:
    mediums = [
        "organic",
        "cpc",
        "referral",
        "email",
        "(none)",
    ]
    data = [
        {"medium": medium, "value": random.randint(100, 1000)} for medium in mediums
    ]
    return data


TOOLTIP_PROPS = {
    "content_style": {
        "backgroundColor": "#1A202C",
        "borderColor": "#4A5568",
        "color": "#E2E8F0",
        "fontSize": "12px",
        "borderRadius": "4px",
    },
    "cursor": {"stroke": "#A0AEC0", "strokeWidth": 1},
    "formatter": "(value, name) => [`${value.toLocaleString()} ${name.split('_')[0]}`, null]",
}


class MarketingDashboardState(rx.State):
    """Holds the state for the marketing dashboard."""

    current_time: str = "Loading..."
    sessions_chart_data: List[Dict[str, Union[str, int]]] = generate_chart_data()
    conversions_chart_data: List[Dict[str, Union[str, int]]] = [
        {
            **d,
            "past_28_days": d["past_28_days"] // 50,
            "prev_28_days": d["prev_28_days"] // 50,
        }
        for d in generate_chart_data()
    ]

    @rx.var
    def sessions_total(self) -> str:
        total = sum((item["past_28_days"] for item in self.sessions_chart_data[:7]))
        return f"{total:,}"

    @rx.var
    def conversions_total(self) -> str:
        total = sum((item["past_28_days"] for item in self.conversions_chart_data[:7]))
        return f"{total:,}"

    google_ads_spent_val: int = 2800
    google_ads_budget_val: int = 5000
    google_ads_conversions_val: int = 85
    google_ads_spent: str = "$2,800"
    google_ads_budget: str = "of $5,000"

    @rx.var
    def google_ads_progress(self) -> float:
        return (
            round(
                self.google_ads_spent_val / self.google_ads_budget_val * 100,
                1,
            )
            if self.google_ads_budget_val > 0
            else 0.0
        )

    @rx.var
    def google_ads_conversions(self) -> int:
        return self.google_ads_conversions_val

    @rx.var
    def google_ads_cpc(self) -> str:
        cpc = (
            self.google_ads_spent_val / self.google_ads_conversions_val
            if self.google_ads_conversions_val > 0
            else 0
        )
        return f"${cpc:.2f}"

    facebook_ads_spent_val: int = 1200
    facebook_ads_budget_val: int = 3000
    facebook_ads_conversions_val: int = 30
    facebook_ads_spent: str = "$1,200"
    facebook_ads_budget: str = "of $3,000"

    @rx.var
    def facebook_ads_progress(self) -> float:
        return (
            round(
                self.facebook_ads_spent_val / self.facebook_ads_budget_val * 100,
                1,
            )
            if self.facebook_ads_budget_val > 0
            else 0.0
        )

    @rx.var
    def facebook_ads_conversions(self) -> int:
        return self.facebook_ads_conversions_val

    @rx.var
    def facebook_ads_cpc(self) -> str:
        cpc = (
            self.facebook_ads_spent_val / self.facebook_ads_conversions_val
            if self.facebook_ads_conversions_val > 0
            else 0
        )
        return f"${cpc:.2f}"

    sessions_by_medium: List[Dict[str, Union[str, int]]] = generate_medium_data()
    conversions_by_medium: List[Dict[str, Union[str, int]]] = [
        {**d, "value": d["value"] // 20} for d in generate_medium_data()
    ]
    google_ads_sessions_val: int = 15000
    google_ads_cpc_val: float = 1.87
    facebook_ads_sessions_val: int = 8000
    facebook_ads_cpc_val: float = 4.0

    @rx.var
    def google_ads_sessions(self) -> str:
        return f"{self.google_ads_sessions_val:,}"

    @rx.var
    def google_ads_sessions_cpc(self) -> str:
        return f"${self.google_ads_cpc_val:.2f}"

    @rx.var
    def facebook_ads_sessions(self) -> str:
        return f"{self.facebook_ads_sessions_val:,}"

    @rx.var
    def facebook_ads_sessions_cpc(self) -> str:
        return f"${self.facebook_ads_cpc_val:.2f}"

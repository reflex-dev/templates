import datetime
import random
from typing import List, TypedDict

import reflex as rx
from faker import Faker

fake = Faker()


class Metric(TypedDict):
    title: str
    value: str
    change: str
    change_direction: str
    description: str
    trend_description: str


class VisitorDataPoint(TypedDict):
    date: str
    series1: int
    series2: int


class DocumentRow(TypedDict):
    id: int
    header: str
    section_type: str
    status: str
    target: int
    limit: int
    reviewer: str


class DashboardState(rx.State):
    """The state for the dashboard page."""

    key_metrics: List[Metric] = []
    visitor_data: List[VisitorDataPoint] = []
    displayed_visitor_data: List[VisitorDataPoint] = []
    document_data: List[DocumentRow] = []
    selected_visitor_timeframe: str = "Last 3 months"
    selected_document_tab: str = "Outline"
    document_columns: List[str] = [
        "",
        "Header",
        "Section Type",
        "Status",
        "Target",
        "Limit",
        "Reviewer",
    ]

    def _generate_fake_data(self):
        """Generates fake data for the dashboard."""
        self.key_metrics = [
            {
                "title": "Total Revenue",
                "value": f"${fake.random_int(min=500000, max=2000000):,}",
                "change": f"+{fake.random_number(digits=2, fix_len=True)}.{fake.random_digit()}%",
                "change_direction": "up",
                "description": "Trending up this month",
                "trend_description": "Visitors for the last 6 months",
            },
            {
                "title": "New Customers",
                "value": f"{fake.random_int(min=500, max=2000):,}",
                "change": f"-{fake.random_number(digits=2, fix_len=True)}%",
                "change_direction": "down",
                "description": f"Down {fake.random_number(digits=2, fix_len=True)}% this period",
                "trend_description": "Acquisition needs attention",
            },
            {
                "title": "Active Accounts",
                "value": f"{fake.random_int(min=30000, max=60000):,}",
                "change": f"+{fake.random_number(digits=2, fix_len=True)}.{fake.random_digit()}%",
                "change_direction": "up",
                "description": "Strong user retention",
                "trend_description": "Engagement exceed targets",
            },
            {
                "title": "Growth Rate",
                "value": f"{fake.random_number(digits=1, fix_len=True)}.{fake.random_digit()}%",
                "change": f"+{fake.random_number(digits=1, fix_len=True)}.{fake.random_digit()}%",
                "change_direction": "up",
                "description": "Steady performance",
                "trend_description": "Meets growth projections",
            },
        ]
        today = datetime.date.today()
        self.visitor_data = []
        for i in range(90):
            date = today - datetime.timedelta(days=i)
            self.visitor_data.append(
                {
                    "date": (
                        date.strftime("Jun %d")
                        if date.month == 6
                        else date.strftime("%b %d")
                    ),
                    "series1": fake.random_int(min=100, max=500),
                    "series2": fake.random_int(min=50, max=300),
                }
            )
        self.displayed_visitor_data = self.visitor_data
        self.visitor_data.reverse()
        statuses = ["Done", "In Process", "Pending"]
        section_types = [
            "Cover page",
            "Table of contents",
            "Narrative",
            "Technical approach",
            "Management plan",
            "Pricing section",
        ]
        self.document_data = []
        for i in range(5):
            self.document_data.append(
                {
                    "id": i,
                    "header": fake.catch_phrase().replace('"', ""),
                    "section_type": random.choice(section_types),
                    "status": random.choice(statuses),
                    "target": fake.random_int(min=5, max=50),
                    "limit": fake.random_int(min=3, max=30),
                    "reviewer": fake.name(),
                }
            )
        self.document_data[0].update(
            {
                "header": "Cover page",
                "section_type": "Cover page",
                "status": "In Process",
                "target": 18,
                "limit": 5,
                "reviewer": "Eddie Lake",
            }
        )
        self.document_data[1].update(
            {
                "header": "Table of contents",
                "section_type": "Table of contents",
                "status": "Done",
                "target": 29,
                "limit": 24,
                "reviewer": "Eddie Lake",
            }
        )
        self.document_data[2].update(
            {
                "header": "Executive summary",
                "section_type": "Narrative",
                "status": "Done",
                "target": 10,
                "limit": 13,
                "reviewer": "Eddie Lake",
            }
        )
        self.document_data[3].update(
            {
                "header": "Technical approach",
                "section_type": "Narrative",
                "status": "Done",
                "target": 27,
                "limit": 23,
                "reviewer": "Jamik Tashpulatov",
            }
        )

    @rx.event
    def load_initial_data(self):
        """Load initial fake data if not already loaded."""
        if (
            not self.key_metrics
            and (not self.visitor_data)
            and (not self.document_data)
        ):
            self._generate_fake_data()

    @rx.event
    def set_visitor_timeframe(self, timeframe: str):
        self.selected_visitor_timeframe = timeframe

        if timeframe == "Last 3 months":
            self.displayed_visitor_data = self.visitor_data

        if timeframe == "Last 30 days":
            self.displayed_visitor_data = self.visitor_data[-30:]

        if timeframe == "Last 7 days":
            self.displayed_visitor_data = self.visitor_data[-7:]

    @rx.event
    def set_document_tab(self, tab: str):
        self.selected_document_tab = tab


TOOLTIP_PROPS = {
    "separator": ": ",
    "cursor": False,
    "is_animation_active": False,
    "label_style": {"fontWeight": "500"},
    "item_style": {
        "color": "currentColor",
        "display": "flex",
        "paddingBottom": "0px",
        "justifyContent": "space-between",
        "textTransform": "capitalize",
    },
    "content_style": {
        "borderRadius": "5px",
        "boxShadow": "0px 2px 6px 0px rgba(0, 0, 0, 0.1)",
        "fontSize": "0.75rem",
        "lineHeight": "1rem",
        "fontWeight": "500",
        "minWidth": "8rem",
        "width": "auto",
        "padding": "0.375rem 0.625rem",
        "backgroundColor": "white",
        "border": "1px solid #e2e8f0",
    },
}
